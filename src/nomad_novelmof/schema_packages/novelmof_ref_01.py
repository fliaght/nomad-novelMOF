import numpy as np
from nomad.metainfo import MSection, Section, Quantity, SubSection
from nomad.datamodel.data import EntryData
from nomad.metainfo import (
    Package,
    Quantity,
    SubSection,
    Section,
)

m_package = Package(name='nomad-novelMOF schema')

class NovelMOF(EntryData):
    '''
    Schema for depositing novel Metal-Organic Framework (MOF) data.
    This schema captures various structural, topological, and physical properties
    of MOFs as derived from experimental or computational studies.
    '''
    m_def = Section(
        a_eln=dict(
            overview=dict(
                sections=[
                    'core_id',
                    'ref_code',
                    'name',
                    'mofid_v2',
                    'pld',
                    'asa',
                    'nasa',
                    'pv',
                    'structure_dimension',
                    'topology_single_nodes',
                    'topology_all_nodes',
                    'catenation',
                    'dimension_by_topology',
                    'hall_symbol',
                    'number_spacegroup',
                    'metal_types',
                    'source',
                    'doi',
                    'year',
                    'publication',
                    'extension',
                    'unmodified',
                    'thermal_stability',
                    'note',
                ]
            )
        )
    )

    core_id = Quantity(
        type=str,
        description='Unique identifier for the MOF, typically a combination of year, metal, topology, and ASR status.',
        a_eln=dict(component='StringEditQuantity', label='Core ID')
    )

    ref_code = Quantity(
        type=str,
        description='Reference code, typically from the Cambridge Structural Database (CSD) or similar databases.',
        a_eln=dict(component='StringEditQuantity', label='Refcode')
    )

    name = Quantity(
        type=str,
        description='Common name or abbreviation of the MOF (e.g., UiO-66, MIL-53).',
        a_eln=dict(component='StringEditQuantity', label='Name')
    )

    mofid_v2 = Quantity(
        type=str,
        description='MOF Identifier v2 string, providing detailed structural and topological information.',
        a_eln=dict(component='StringEditQuantity', label='MOFid-v2')
    )

    pld = Quantity(
        type=np.float64,
        unit='angstrom',
        description='Pore Limiting Diameter (PLD) of the MOF, representing the smallest pore aperture.',
        a_eln=dict(component='NumberEditQuantity', label='PLD (Å)')
    )

    asa = Quantity(
        type=np.float64,
        unit='m**2 / cm**3',
        description='Accessible Surface Area (ASA) per unit volume of the MOF.',
        a_eln=dict(component='NumberEditQuantity', label='ASA (m²/cm³)')
    )

    nasa = Quantity(
        type=np.float64,
        unit='m**2 / cm**3',
        description='Non-Accessible Surface Area (NASA) per unit volume of the MOF.',
        a_eln=dict(component='NumberEditQuantity', label='NASA (m²/cm³)')
    )

    pv = Quantity(
        type=np.float64,
        unit='cm**3 / g',
        description='Pore Volume (PV) per unit mass of the MOF.',
        a_eln=dict(component='NumberEditQuantity', label='PV (cm³/g)')
    )

    structure_dimension = Quantity(
        type=np.int32,
        description='The structural dimension of the MOF (e.g., 0D, 1D, 2D, or 3D).',
        a_eln=dict(component='NumberEditQuantity', label='Structure Dimension')
    )

    topology_single_nodes = Quantity(
        type=str,
        description='Topology of the MOF based on single nodes (e.g., rtl, fcu, bpq).',
        a_eln=dict(component='StringEditQuantity', label='Topology (Single Nodes)')
    )

    topology_all_nodes = Quantity(
        type=str,
        description='Topology of the MOF based on all nodes (e.g., rtl, fcu, rna).',
        a_eln=dict(component='StringEditQuantity', label='Topology (All Nodes)')
    )

    catenation = Quantity(
        type=np.int32,
        description='The degree of interpenetration or catenation in the MOF structure.',
        a_eln=dict(component='NumberEditQuantity', label='Catenation')
    )

    dimension_by_topology = Quantity(
        type=np.int32,
        description='The dimension derived from the MOF\'s topology.',
        a_eln=dict(component='NumberEditQuantity', label='Dimension by Topology')
    )

    hall_symbol = Quantity(
        type=str,
        description='The Hall symbol representing the space group symmetry of the MOF.',
        a_eln=dict(component='StringEditQuantity', label='Hall Symbol')
    )

    number_spacegroup = Quantity(
        type=np.int32,
        description='The International Union of Crystallography (IUCr) space group number.',
        a_eln=dict(component='NumberEditQuantity', label='Number Spacegroup')
    )

    metal_types = Quantity(
        type=str,
        description='Types of metal elements present in the MOF (e.g., Co, Zr, Fe), comma-separated if multiple.',
        a_eln=dict(component='StringEditQuantity', label='Metal Types')
    )

    source = Quantity(
        type=str,
        description='The origin of the MOF data (e.g., CSD - Cambridge Structural Database, SI - Supplementary Information).',
        a_eln=dict(component='StringEditQuantity', label='Source')
    )

    doi = Quantity(
        type=str,
        description='Digital Object Identifier (DOI) of the scientific publication where the MOF data was reported.',
        a_eln=dict(component='StringEditQuantity', label='DOI')
    )

    year = Quantity(
        type=np.int32,
        description='The year of publication for the MOF data.',
        a_eln=dict(component='NumberEditQuantity', label='Year')
    )

    publication = Quantity(
        type=str,
        description='The name of the journal or publisher where the MOF data was published (e.g., RSC, ACS).',
        a_eln=dict(component='StringEditQuantity', label='Publication')
    )

    extension = Quantity(
        type=str,
        description='Additional details or specific processing conditions, e.g., "All Solvent Removed".',
        a_eln=dict(component='StringEditQuantity', label='Extension')
    )

    unmodified = Quantity(
        type=bool,
        description='A boolean flag indicating whether the MOF is in its unmodified state (True/False).',
        a_eln=dict(component='BoolEditQuantity', label='Unmodified')
    )

    thermal_stability = Quantity(
        type=np.float64,
        unit='celsius',
        description='Thermal stability of the MOF, typically measured as the decomposition temperature.',
        a_eln=dict(component='NumberEditQuantity', label='Thermal Stability (℃)')
    )

    note = Quantity(
        type=str,
        description='Any additional notes or comments relevant to the MOF entry.',
        a_eln=dict(component='StringEditQuantity', label='Note')
    )
m_package.__init_metainfo__()