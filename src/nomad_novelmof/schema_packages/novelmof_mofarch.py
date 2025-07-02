from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage, MEnum # 导入 MEnum 用于定义枚举类型
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Datetime, MEnum, Quantity, Section, SubSection,JSON

configuration = config.get_plugin_entry_point(
    'nomad_novelmof.schema_packages:novel_mof_schema'
)

m_package = SchemaPackage()


class CompositionalInformation(ArchiveSection):
    '''
    Compositional details of the MOF.
    '''
    metal_types = Quantity(
        type=str,
        description="Type(s) of metal present in the MOF (e.g., Ga, Dy, Cu).",
    )


class PoreCharacteristics(ArchiveSection):
    '''
    Pore characteristics of the MOF structure.
    '''
    PLD_angstrom = Quantity( # Corrected: PLD_angstrom
        type=np.float64,
        unit='angstrom',
        description="Pore Limiting Diameter (PLD) in Angstroms.",
    )
    ASA_m2_cm3 = Quantity( # Corrected: ASA_m2_cm3
        type=np.float64,
        unit='m**2/cm**3',
        description="Accessible Surface Area (ASA) per unit volume.",
    )
    NASA_m2_cm3 = Quantity( # Corrected: NASA_m2_cm3
        type=np.float64,
        unit='m**2/cm**3',
        description="Non-Accessible Surface Area (NASA) per unit volume.",
    )
    PV_cm3_g = Quantity( # Corrected: PV_cm3_g
        type=np.float64,
        unit='cm**3/g',
        description="Pore Volume (PV) per unit mass."
    )


class TopologicalAndCrystallographicInformation(ArchiveSection):
    '''
    Topological and crystallographic details of the MOF.
    '''
    structure_dimension = Quantity(
        type=int,
        description="Dimensionality of the MOF structure (e.g., 2 for 2D, 3 for 3D)."
    )
    topology_single_nodes = Quantity(
        type=str,
        description="Topology based on single nodes (e.g., bpq, pcu)."
    )
    topology_all_nodes = Quantity(
        type=str,
        description="Topology based on all nodes."
    )
    catenation = Quantity(
        type=int,
        description="Degree of catenation of the MOF structure."
    )
    dimension_by_topo = Quantity(
        type=int,
        description="Dimensionality derived from the topology."
    )
    hall = Quantity(
        type=str,
        description="Hall symbol for the space group."
    )
    number_spacegroup = Quantity(
        type=int,
        description="International Union of Crystallography (IUC) space group number."
    )


class StructuralProperties(ArchiveSection):
    '''
    Structural properties of the MOF.
    '''
    pore_characteristics = SubSection(
        section_def=PoreCharacteristics,
        description="Characteristics related to the pores of the MOF."
    )
    topological_and_crystallographic_information = SubSection(
        section_def=TopologicalAndCrystallographicInformation,
        description="Information on the topology and crystallography of the MOF."
    )


class Stability(ArchiveSection):
    '''
    Stability information of the MOF.
    '''
    thermal_stability_celsius = Quantity(
        type=np.float64,
        unit='celsius',
        description="Thermal stability temperature in degrees Celsius."
    )


class CalculationalStructuralPropertiesAndStability(ArchiveSection):
    '''
    Calculational structural properties and stability of the MOF.
    '''
    structural_properties = SubSection(
        section_def=StructuralProperties,
        description="Calculated structural properties."
    )
    stability = SubSection(
        section_def=Stability,
        description="Stability information, e.g., thermal stability."
    )


class StructuralData(ArchiveSection):
    '''
    Structural data including modification status and CIF.
    '''
    unmodified = Quantity(
        type=bool,
        description="Boolean indicating if the MOF is unmodified (TRUE/FALSE)."
    )
    cif_data = Quantity(
        type=str, # Or MProxy('nomad.datamodel.results.Symmetry') if you want to store parsed CIF data
        description="Crystallographic Information File (CIF) data."
    )


class ReferenceData(ArchiveSection):
    '''
    Reference data for the MOF, typically publication details.
    '''
    year = Quantity(
        type=int,
        description="Year of publication."
    )
    publication = Quantity(
        type=str,
        description="Journal or publication venue (e.g., ACS, RSC)."
    )
    doi = Quantity(
        type=str,
        description="Digital Object Identifier (DOI) for the source publication."
    )


class SynthesisParameter(ArchiveSection):
    '''
    Parameters used during synthesis.
    '''
    temperature = Quantity(
        type=np.float64, # Assuming parse_temperature converts to float
        unit="celsius",
        description="Synthesis temperature."
    )
    time = Quantity(
        type=np.float64, # Assuming parse_time converts to float in hours
        unit="hour",
        description="Synthesis time."
    )


class SynthesisInformation(ArchiveSection):
    '''
    Details about the synthesis process.
    '''
    synthesis_method = Quantity(
        type=str,
        description="Method used for MOF synthesis (e.g., solvothermal synthesis, chemical synthesis)."
    )
    synthesis_parameter = SubSection(
        section_def=SynthesisParameter,
        description="Parameters specific to the synthesis method."
    )


class MOFArchive(Schema):
    '''
    A schema describing structural, synthesis, and calculational properties of Metal-Organic Frameworks (MOFs)
    based on the CoReMOF database.
    '''
    CoReID = Quantity(
        type=str,
        description="Unique identifier for the MOF core structure."
    )
    CSD_refcode = Quantity(
        type=str,
        description="CSD reference code for the MOF."
    )
    common_name = Quantity(
        type=str,
        description="Common name or abbreviation of the MOF."
    )
    MOFID_v2 = Quantity(
        type=str,
        description="MOFid-v2 string for detailed structural identification."
    )
    transcriber = Quantity(
        type=str,
        shape=['*'],
        description="Names of staffs who transcribed the data."
    )
    compositional_information = SubSection(
        section_def=CompositionalInformation,
        description="Information about the chemical composition of the MOF."
    )
    calculational_structural_properties_and_stability = SubSection(
        section_def=CalculationalStructuralPropertiesAndStability,
        description="Calculated structural properties and stability data."
    )
    structural_data = SubSection(
        section_def=StructuralData,
        description="Raw and processed structural data of the MOF."
    )
    reference_data = SubSection(
        section_def=ReferenceData,
        description="Bibliographic reference information for the MOF entry."
    )
    synthesis_information = SubSection(
        section_def=SynthesisInformation,
        description="Detailed information about the synthesis of the MOF."
    )


m_package.__init_metainfo__()