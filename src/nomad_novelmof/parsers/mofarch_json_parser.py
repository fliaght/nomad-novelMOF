import json
import numpy as np
from typing import TYPE_CHECKING, Optional

from jmespath import search
from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser

from nomad_novelmof.parsers.utils import create_archive

from nomad_novelmof.schema_packages.novelmof_mofarch import (
MOFArchive,
)

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger

# parser的工作流是怎么样的？
## MOFArchJsParserEntryPoint 中内置对于文件的检测判断，决定是否启动该项ParserEntryPoint ，同时内部调用相对应的Parser进行处理
# parser的工作流是：
## 读取文件并将相应内容转化到对应的schema中
## 福哦一个




#
# def get_id_from_mainfile(mainfile: str) -> str:
#     """
#     Extracts the ID from the mainfile name.
#     The ID is expected to be the first part of the filename, separated by an .
#     """
#     try:
#         return os.path.splitext(mainfile)[0].split('.')[0]
#     except IndexError:
#         raise ValueError(f'Invalid filename format: {mainfile}')
#
# def get_eln_archive_name(mainfile: str) -> str:
#     """
#     Returns the name of the archive file for the ELN.
#     The name is generated based on the mainfile name.
#     """
#     return f'mofarch_{get_id_from_mainfile(mainfile)}.archive.json'



class MOFArchJsParser(MatchingParser):
    """
    Parser for MOFArch JSON files and creating instances of MOFArchive.

    ref perovskite_solar_cell_database.parsers.tandem_json_parser.TandemJSONParser
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:

        # Load the JSON file
        with open(mainfile) as file:
            source_dict = json.load(file)

        update_dict = self.map_json_to_schema_with_type_check(source_dict,logger)
        mof_entry = MOFArchive()
        mof_entry.m_update_from_dict(update_dict)

        archive.data = mof_entry



        # # Question: what does this do?
        # archive.data = RawFileMOFArchJson(
        #     tandem=create_archive(tandem, archive, get_eln_archive_name(mainfile)),
        #     data=source_dict,
        # )
        # archive.metadata.entry_name = f'MOF Arch {id} data file'



    @staticmethod
    def map_json_to_schema_with_type_check(source: dict,logger) -> dict:
        """
        Maps the JSON data to the MOFArchive schema using search calls,
        with robust type checking and conversion.
        """

        def search(path: str, data: dict, default=None, expected_type=None) -> Optional[object]:
            """
            Safely retrieves a value from a nested dictionary using a dot-separated path.
            Logs an INFO message if a key in the path is not found.
            Performs type checking and conversion for float and int types.
            """
            keys = path.split('.')
            current = data
            for i, key in enumerate(keys):
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    logger.info(f"Key '{key}' not found in path '{path}'. Returning default value '{default}'.")
                    return default

            # Value found, now perform type checking and conversion if expected_type is provided
            if expected_type:
                # Handle specific numpy types for float/int if needed, map them to Python built-in types for isinstance check
                # For assignment, we will still use the original numpy type as specified in schema
                check_type = None
                if expected_type in [float, np.float64, np.float32]:
                    check_type = float
                elif expected_type in [int, np.int64, np.int32]:
                    check_type = int
                elif expected_type == bool:
                    check_type = bool
                elif expected_type == str:
                    check_type = str

                if check_type:
                    if current is None:  # Allow None if the schema permits (e.g., cif_data)
                        return default
                    try:
                        if not isinstance(current, check_type):
                            logger.warning(
                                f"Type mismatch for '{path}': Expected {expected_type.__name__}, got {type(current).__name__}. "
                                f"Attempting to convert."
                            )
                            # Attempt conversion
                            if check_type == float:
                                current = float(current)
                            elif check_type == int:
                                current = int(current)
                            elif check_type == bool:
                                # Convert common string representations of boolean
                                if isinstance(current, str):
                                    if current.lower() in ['true', '1', 'yes']:
                                        current = True
                                    elif current.lower() in ['false', '0', 'no']:
                                        current = False
                                    else:
                                        raise ValueError(f"Cannot convert string '{current}' to boolean.")
                                else:
                                    current = bool(current)
                            elif check_type == str:
                                current = str(current)
                            elif check_type == list:
                                if isinstance(current, str):
                                    try:
                                        # Attempt to parse as a literal list string
                                        import ast
                                        converted_list = ast.literal_eval(current)
                                        if isinstance(converted_list, list):
                                            current = converted_list
                                        else:
                                            # If not a list, treat as a comma-separated string
                                            current = [item.strip() for item in current.replace(' and ', ',').split(',') if item.strip()]
                                    except (ValueError, SyntaxError):
                                        # Fallback for simple comma-separated strings if literal_eval fails
                                        current = [item.strip() for item in current.replace(' and ', ',').split(',') if item.strip()]
                                else:
                                    raise ValueError(f"Cannot convert type {type(current).__name__} to list.")
                        # If it's a numpy type, convert if the original was a Python built-in type that passed check
                        if expected_type in [np.float64, np.float32] and not isinstance(current, np.floating):
                            current = expected_type(current)
                        elif expected_type in [np.int64, np.int32] and not isinstance(current, np.integer):
                            current = expected_type(current)

                    except (ValueError, TypeError) as e:
                        logger.error(
                            f"Failed to convert value '{current}' (type {type(current).__name__}) at path '{path}' to {expected_type.__name__}: {e}")
                        return default  # Return default if conversion fails

            return current



        data = {}

        # Top-level properties
        data['common_name'] = search('common_name', source, expected_type=str)
        data['identifier'] = search('identifier', source, expected_type=str)

        # Transcriber: Handle list conversion if it's a string
        transcriber_val = search('transcriber', source)
        if isinstance(transcriber_val, str):
            transcriber_val = transcriber_val.replace(' and ', ',')
            transcriber_val = [t.strip() for t in transcriber_val.split(',') if t.strip()]
        data['transcriber'] = transcriber_val  # The schema defines it as shape=['*'], so keep it a list

        # Compositional Information
        data['compositional_information'] = {
            'metal_types': search('compositional_information.metal_types', source, expected_type=list),
        }

        # Calculational Structural Properties and Stability
        data['calculation_properties'] = {
            "structural_properties": {
                'pore_characteristics': {
                    "PLD_angstrom": search(
                        'calculation_properties.structural_properties.pore_characteristics.PLD_angstrom',
                        source, expected_type=float),
                    "ASA_m2_cm3": search(
                        'calculation_properties.structural_properties.pore_characteristics.ASA_m2_cm3',
                        source, expected_type=float),
                    "NASA_m2_cm3": search(
                        'calculation_properties.structural_properties.pore_characteristics.NASA_m2_cm3',
                        source, expected_type=float),
                    "PV_cm3_g": search(
                        'calculation_properties.structural_properties.pore_characteristics.PV_cm3_g',
                        source, expected_type=float),
                },
                'topological_and_crystallographic_information': {
                    "structure_dimension": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.structure_dimension',
                        source, expected_type=int),
                    "topology_single_nodes": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.topology_single_nodes',
                        source, expected_type=str),
                    "topology_all_nodes": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.topology_all_nodes',
                        source, expected_type=str),
                    "catenation": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.catenation',
                        source, expected_type=int),
                    "dimension_by_topo": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.dimension_by_topo',
                        source, expected_type=int),
                    "hall": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.hall',
                        source, expected_type=str),
                    "number_spacegroup": search(
                        'calculation_properties.structural_properties.topological_and_crystallographic_information.number_spacegroup',
                        source, expected_type=int),
                }
            },
            'stability': {
                "thermal_stability_celsius": search(
                    'calculation_properties.stability.thermal_stability_celsius', source,
                    expected_type=float),
            },
        }

        # Structural Data
        data['structural_data'] = {
            "unmodified": search('structural_data.unmodified', source, expected_type=bool),
            "cif_data": search('structural_data.cif_data', source, expected_type=str),
            # Can be null, so str is fine if None
        }

        # Reference Data
        data['reference_data'] = {
            "year": search('reference_data.year', source, expected_type=str),
            "publication": search('reference_data.publication', source, expected_type=str),
            "doi": search('reference_data.doi', source, expected_type=str),
        }

        # Synthesis Information
        data['synthesis_information'] = {
            "synthesis_method": search('synthesis_information.synthesis_method', source, expected_type=str),
            "synthesis_parameter": {
                "starting_materials": search('synthesis_information.synthesis_parameter.starting_materials', source,expected_type=list),
                "temperature": search('synthesis_information.synthesis_parameter.temperature.normalized_c', source,
                                      expected_type=float),
                "time": search('synthesis_information.synthesis_parameter.time.normalized_h', source,
                               expected_type=float),
            }
        }

        return data