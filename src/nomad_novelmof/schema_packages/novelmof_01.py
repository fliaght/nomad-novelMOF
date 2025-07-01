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
from nomad.metainfo import Datetime, MEnum, Quantity, Section, SubSection

configuration = config.get_plugin_entry_point(
    'nomad_novelmof.schema_packages:novel_mof_schema'
)

m_package = SchemaPackage()

class SynthesisData(ArchiveSection):
    synthesis_method = Quantity(
        type=str, # Could be MEnum if you have a predefined list
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Method used for MOF synthesis (e.g., solvothermal synthesis, chemical synthesis)."
    )

    synthesis_temperature = Quantity(
        type=str, # Stored as string to accommodate varied formats like "room temperature", "120°C"
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Synthesis temperature."
    )

    synthesis_time = Quantity(
        type=str, # Stored as string to accommodate varied formats like "3 days", "1 h", "48h"
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Synthesis time."
    )

class PublicationData(ArchiveSection):
    DOI = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Digital Object Identifier (DOI) for the source publication."
    )

    pulication_year = Quantity(
        type=int,
        description="Year of publication."
    )

    publisher = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Journal or publication venue (e.g., ACS, RSC)."
    )
class CoReMOFData(ArchiveSection):
    PLD_angstrom = Quantity( # Changed to include unit in name for clarity
        type=np.float64,
        unit='angstrom', # Å (Angstrom)
        description="Pore Limiting Diameter (PLD) in Angstroms.",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    ASA_m2_cm3 = Quantity( # Changed to include unit in name for clarity
        type=np.float64,
        unit='m^2/cm^3',
        description="Accessible Surface Area (ASA) per unit volume.",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    NASA_m2_cm3 = Quantity( # Changed to include unit in name for clarity
        type=np.float64,
        unit='m^2/cm^3',
        description="Non-Accessible Surface Area (NASA) per unit volume.",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    PV_cm3_g = Quantity( # Changed to include unit in name for clarity
        type=np.float64,
        unit='cm^3/g',
        description="Pore Volume (PV) per unit mass."
    )

    structure_dimension = Quantity(
        type=int,
        description="Dimensionality of the MOF structure (e.g., 2 for 2D, 3 for 3D)."
    )

    topology_SingleNodes = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Topology based on single nodes (e.g., bpq, pcu)."
    )

    topology_AllNodes = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
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
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Hall symbol for the space group."
    )

    number_spacegroup = Quantity(
        type=int,
        description="International Union of Crystallography (IUC) space group number."
    )

    metal_types = Quantity(
        type=str, # Could be MEnum if you have a predefined list, or a list of strings
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Type(s) of metal present in the MOF (e.g., Ga, Dy, Cu)."
    )

    unmodified = Quantity(
        type=bool,
        description="Boolean indicating if the MOF is unmodified (TRUE/FALSE)."
    )

    thermal_stability_celsius = Quantity( # Changed to include unit in name for clarity
        type=np.float64,
        unit='celsius', # ℃ (Celsius)
        description="Thermal stability temperature in degrees Celsius."
    )

class MOFArchive(Schema):
    """
    A schema describing structural and synthesis properties of Metal-Organic Frameworks (MOFs)
    """

    coreid = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Unique identifier for the MOF core structure."
    )

    CSD_refcode = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Reference code for the MOF, often from a database."
    )

    common_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Common name or abbreviation of the MOF."
    )

    mofid_v2 = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="MOFid-v2 string for detailed structural identification."
    )

    # General information
    coro_mof_data = SubSection(
        section_def=CoReMOFData, description='Calculation Data from CoRe MOF DB.'
    )

    synthesis_data_1 = SubSection(
        section_def=SynthesisData, description='Synthesis data from calculation.'
    )

    reference_data = SubSection(
        section_def=PublicationData, description='publication information data from publication.'
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        # logger.info('MOFProperties.normalize', parameter=configuration.parameter if configuration else "No configuration")

m_package.__init_metainfo__()