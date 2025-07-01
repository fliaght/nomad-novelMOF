import pandas as pd
from typing import TYPE_CHECKING
from nomad_novelmof.schema_packages.novelmof_01 import MOFArchive
import re

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.config import config
from nomad.parsing.parser import MatchingParser

#configuration = config.get_plugin_entry_point('schema_package_entry_point')
configuration = None
if hasattr(config, "get_plugin_entry_point") and callable(config.get_plugin_entry_point):
    configuration = config.get_plugin_entry_point('schema_package_entry_point')


unit_pattern = re.compile(
    r'^(\d+(\.\d+)?|\.\d+)([eE][-+]?\d+)?\s*\w+([*/^]\w+)*(\s*[/()]\s*\w+)*$'
)  # Matches ".9kg", "10mA", "1.5 kg", "2 cm^2/(V*s)", "1e-6 m" etc.

def partial_get(data, label, default=None):
    """
    Retrieve a value from a DataFrame or Series based on a partial match of the label.

    Parameters:
    data (pd.DataFrame or pd.Series): The data source to search within.
    label (str): The label to partially match against the index of the data.
    default (any, optional): The default value to return if no match is found. Defaults to None.

    Returns:
    any: The matched value from the data, converted if specified, or the default value if no match is found.
    """

    df_matched = data[data.index.str.contains(label)]
    if df_matched.empty:
        return default

    if isinstance(data, pd.DataFrame):
        value = df_matched.iloc[0, 0]
    elif isinstance(data, pd.Series):
        value = df_matched.iloc[0]
    else:
        return default

    return value.strip() if isinstance(value, str) else value




class MOFArchXLSParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('BatteryParser.parse', parameter=configuration.parameter)

        # reading CSV file
        try:
            df = pd.read_excel(mainfile)
        except Exception as e:
            logger.error(f"Failed to read excel file: {e}")
            return

        # dictionary to store material data
        MOFarch_data = {}

        # iterate over rows and create BatteryProperties sections
        for _, row in df.iterrows():
            material_name = row.get("Name", "Unknown Material")
            property_type = row.get("Property")
            value = row.get("Value")
            doi = row.get("DOI", "No DOI Available")
            journal = row.get("Journal", "Unknown Journal")

            # check material entry if not exists
            if material_name not in MOFarch_data:
                MOFarch_data[material_name] = archive.m_create(MOFarch_data)
                MOFarch_data[material_name].material_name = material_name
                MOFarch_data[material_name].DOI = doi
                MOFarch_data[material_name].journal = journal
                #print(battery_data[material_name].material_name)

            # check extracted values based on property type
            if property_type == "Capacity":
                battery_data[material_name].capacity = float(value) if pd.notna(value) else None
            elif property_type == "Voltage":
                battery_data[material_name].voltage = float(value) if pd.notna(value) else None
            elif property_type == "Coulombic Efficiency":
                battery_data[material_name].coulombic_efficiency = float(value) if pd.notna(value) else None
            elif property_type == "Energy Density":
                battery_data[material_name].energy_density = float(value) if pd.notna(value) else None
                #print(battery_data[material_name].energy_density)
            elif property_type == "Conductivity":
                battery_data[material_name].conductivity = float(value) if pd.notna(value) else None

        # log the parsed data
        for material, entry in battery_data.items():
            logger.info(f"Parsed entry: {material}, {entry.capacity}, {entry.voltage}")