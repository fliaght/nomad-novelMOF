#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import numpy as np
from nomad.metainfo import ( Package, Quantity, SubSection, Section)
from nomad.datamodel.data import EntryData, ArchiveSection, UseCaseElnCategory
from nomad.datamodel.metainfo.eln import PublicationReference
from nomad.datamodel.metainfo.basesections import PubChemPureSubstanceSection
from nomad.datamodel.results import Material
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
import ase
from nomad.normalizing import normalizers
from nomad.units import ureg
from nomad.datamodel.metainfo import runschema
# from nomad.normalizing.common import load_structure_file
from nomad.normalizing.porosity import create_topology_porosity
# from nomad.datamodel.results import Material
# from nomad.atomutils import load_structure_file
m_package = Package(name='MOF Parser', version='version_0.0.1')


# class MofAtoms(ArchiveSection):
#     """
#     A base section for for parsing crystal structure files, e.g. `.cif`, and
#     populating the Material section in Results.
#     """

#     structure_file = Quantity(
#         type=str,
#         description='The structure file.',
#         a_eln=dict(component='FileEditQuantity'),
#     )

#     def normalize(self, archive, logger):
#         super(MofAtoms, self).normalize(archive, logger)

#         if self.structure_file:
#             from ase.io import read
#             from nomad.normalizing.results import ResultsNormalizer
#             from nomad.normalizing.porosity import PorosityNormalizer
#             from nomad.normalizing.system import SystemNormalizer
#             from nomad.normalizing.optimade import OptimadeNormalizer
#             from nomad.datamodel.metainfo.simulation.run import Run
#             from nomad.datamodel.metainfo.simulation.run import Program

#             with archive.m_context.raw_file(self.structure_file) as f:
#                 try:
#                     structure = read(f.name)
#                     print (structure)
#                 except Exception as e:
#                     raise ValueError('could not read structure file') from e

#                 run = Run()
#                 archive.run = [run]
#                 system = SystemTheory()
#                 system.atoms = Atoms()
#                 try:
#                     system.atoms.lattice_vectors = structure.get_cell() * ureg.angstrom
#                 except Exception as e:
#                     logger.warn(
#                         'Could not parse lattice vectors from structure file.',
#                         exc_info=e,
#                     )
#                 system.atoms.labels = structure.get_chemical_symbols()
#                 system.atoms.positions = structure.get_positions() * ureg.angstrom
#                 try:
#                     system.atoms.periodic = structure.get_pbc()
#                 except Exception as e:
#                     logger.warn(
#                         'Could not parse periodicity from structure file.', exc_info=e
#                     )
#                     system.atoms.periodic = [True, True, True]
#                 system.atoms.species = structure.get_atomic_numbers()
#                 archive.run[0].system = [system]
#                 program = Program()
#                 archive.run[0].program = program
#                 archive.run[0].program.name = 'Structure File Importer'
#                 system_normalizer = SystemNormalizer(archive)
#                 system_normalizer.normalize()
#                 porosity_normalizer= PorosityNormalizer(archive)
#                 porosity_normalizer.normalize()
#                 optimade_normalizer = OptimadeNormalizer(archive)
#                 optimade_normalizer.normalize()
#                 results_normalizer = ResultsNormalizer(archive)
#                 results_normalizer.normalize()

#         # TODO: rewrite it in a way in which the run section is not needed and System is
#         # directly added to the archive.data
#         # set run to None if exist
#         if archive.run:
#             archive.run = None


def load_structure_file(upload_file):
    """
    Function to read an upload file using ase,
    convert it into a nomad atom and then parse
    it to a system
    """
    read_atom = ase.io.read(upload_file)
    atoms = runschema.system.Atoms()
    system = runschema.system.System(atoms=atoms)
    system.atoms.positions = read_atom.get_positions() * ureg.angstrom
    system.atoms.labels = read_atom.get_chemical_symbols()
    system.atoms.atomic_numbers = read_atom.get_atomic_numbers()
    system.atoms.species = read_atom.get_atomic_numbers()
    system.atoms.lattice_vectors = read_atom.get_cell() * ureg.angstrom
    system.atoms.periodic = read_atom.get_pbc()
    return system

class TimeQuantity(ArchiveSection):
    """
    The concentration and unit of each reagent used
    """
    value = Quantity(
        type=np.dtype(np.float64),
        unit='hr',
        description="""
        The time in hours
        """,
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit="hr")
    )
    flag = Quantity(
        type=str,
        description="""
        If a flag is provided, it implies that the time has been converted into
        hours based on the results from the survey.
        """,
        a_eln=dict(component='StringEditQuantity')
    )

class ReagentQuantities(ArchiveSection):
    """
    The concentration and unit of each reagent used
    """
    m_def = Section(label_quantity="mof_reagent_name")

    mof_reagent_name = Quantity(
        type=str,
        description="""
        The name of the reagent used in synthesis. This could be the
        metal precursor, organic ligand or solvent.
        """,
        a_eln=dict(component='StringEditQuantity')
    )

    mass = Quantity(
        type=np.dtype(np.float64),
        unit='g',
        description='The mass of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='g'
        ),
    )

    volume = Quantity(
        type=np.dtype(np.float64),
        unit='litre',
        description='The volume of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='ml'
        ),
    )

    moles = Quantity(
        type=np.dtype(np.float64),
        unit='moles',
        description='The moles of the MOF reagent',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='millimol'
        ),
    )

    molar_concentration = Quantity(
        type=np.dtype(np.float64),
        unit='molar',
        description='The concentration of the MOF reagent',
        a_eln=ELNAnnotation(
             component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='molar'
        ),
    )


class ExperimentalData(ArchiveSection):
    """
    Experimental data extracted from the Cambridge structural database and from
    journal articles downloaded using the DOI of each MOF extracted from the Cambridge
    structural database. The names of the organic ligands have been intelligently
    extracted from the IUPAC name of each MOF provided in the Cambridge structural database
    and the metal salt, solvent and temperature were computed extracted from journal articles
    using the chemicaldataextractor. The output from the chemical data extractor were process
    to ensure acurate extraction of exact synthetic parameter for each system. Consequently, this
    class maps structures to experimental synthetic conditions
    """

    mof_synthesis_method = Quantity(
        type=str,
        description='Experimental method use in synthesising the MOF',
        a_eln=dict(component='EnumEditQuantity'),
    )

    mof_metal_precursor = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_organic_linker_reagent = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_solvent = SubSection(
        section_def=PubChemPureSubstanceSection, repeats=True)

    mof_reaction_quanties = SubSection(
        section_def=ReagentQuantities, repeats=True
    )

    mof_reaction_time = SubSection(
        section_def=TimeQuantity, repeats=True
    )

    mof_reaction_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The temperature at which the reaction takes place. The temperature at which the reaction vessel was heated",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_crystallization_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="Temeprature at which the sample was heated to before crystallization started",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_melting_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The recorded temperature at which the MOF solid turned to liquid",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_stability_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="The recorded temperature at which the MOF decomposes",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_drying_temperature = Quantity(
        type=np.dtype(np.float64),
        unit='kelvin',
        shape=['*'],
        description="Temperature at which the MOF was heated to remove all guest molecules",
        a_eln=dict(component='NumberEditQuantity'),
    )

    mof_synthesis_precaution = Quantity(
        type=str,
        description="Hazard statement, which users should to take into consideration before performing synthesis",
        a_eln=dict(component='RichTextEditQuantity'),
    )


class GeneralMOFData(ArchiveSection):
    """
    General information about MOFs. Some extracted directly from the CSD database
    and others extracted from structural manipulation
    """
    mof_alias = Quantity(
        type=str,
        shape=['*'],
        description='Nickname given to the MOF from the CSD',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_r_factor = Quantity(
        type=np.dtype(np.float64),
        description='The r-factor of the crystal, which is a measure of how well the refined structure matches the powder diffraction pattern',
        a_eln=dict(component='NumberEditQuantity')
    )

    mof_iupac_name = Quantity(
        type=str,
        description="The exact IUPAC name of the MOF extracted from the CSD. Note that there are some errors in the name. So care should be take when using this names since there are a couple of typos",
        a_eln=dict(component='StringEditQuantity')
    )

    mof_topology = Quantity(
        type=str,
        shape=['*'],
        description='Three letter topological symbol obtained from RSCR. This was computed using MOFid python script. We an inbuit implemetation for topological calculation is currently being implement in NOMAD',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_color = Quantity(
        type=str,
        description='colour of the MOF',
        a_eln=dict(component='StringEditQuantity')
    )


class Citation(PublicationReference):
    pass


class MOFData(EntryData):
    '''
    '''
    m_def = Section(
        label='MOF Synthetic Condition',
        categories=[UseCaseElnCategory])

    data_authors = Quantity(
        type=str,
        shape=['*'],
        description='The authors',
        a_eln=dict(component='StringEditQuantity', overview=True))

    mof_identifier = Quantity(
        type=str,
        description='The unique identifier for the system in the cambridge structural database',
        a_eln=dict(component='StringEditQuantity')
    )

    mof_source = Quantity(
        type=str,
        description='The source of the MOF',
        a_eln=dict(component='StringEditQuantity'),
    )

    institute = Quantity(
        type=str,
        shape=["*"],
        description='Alias/short name of the home institute of the owner, e.g. `KIT`.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity)
        )

    structure_file = Quantity(
        type=str,
        description='The structure file.',
        a_eln=dict(component='FileEditQuantity', overview=True),
    )

    mof_generalities=SubSection(section_def=GeneralMOFData)
    mof_experimental_synthetic_condition=SubSection(
        section_def=ExperimentalData)
    citation=SubSection(section_def=Citation)

    def normalize(self, archive, logger):
        super(MOFData, self).normalize(archive, logger)
        if self.structure_file:
            with archive.m_context.raw_file(self.structure_file) as f:
                try:
                    system =  load_structure_file(f.name)
                except Exception as e:
                    raise ValueError('could not read structure file') from e
            if system.atoms:
                run = runschema.run.Run()
                run.system.append(system)
                archive.run.append(run)
                system_normalizer = None
                for normalizer in normalizers:
                    if normalizer.python_package == 'systemnormalizer':
                        system_normalizer = normalizer
                        break
                    if system_normalizer is not None:
                        system_normalizer(archive).normalize()

                created_system = create_topology_porosity(system)
                material = archive.m_setdefault('results.material')
                if created_system:
                    for system in created_system:
                        material.m_add_sub_section(Material.topology, system)


m_package.__init_metainfo__()