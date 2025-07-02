from nomad.config.models.plugins import SchemaPackageEntryPoint
# from pydantic import Field
#
#
# class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')
#
#     def load(self):
#         from nomad_novelmof.schema_packages.schema_package import m_package
#
#         return m_package


# schema_package_entry_point = NewSchemaPackageEntryPoint(
#     name='NewSchemaPackage',
#     description='New schema package entry point configuration.',
# )

class NovelMOFSchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_novelmof.schema_packages.novelmof_mofarch import m_package

        return m_package


novel_mof_schema = NovelMOFSchemaEntryPoint(
    name='novel MOF Schema',
    description='A module containing schemas for Schema package for describing MOF structural and synthesis properties.',
)