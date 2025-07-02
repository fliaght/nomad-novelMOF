from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


# class NewParserEntryPoint(ParserEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')
#
#     def load(self):
#         from nomad_novelmof.parsers.parser import NewParser
#
#         return NewParser(**self.model_dump())
#
#
# parser_entry_point = NewParserEntryPoint(
#     name='NewParser',
#     description='New parser entry point configuration.',
#     mainfile_name_re=r'.*\.newmainfilename',
# )

# from nomad.config.models.plugins import ParserEntryPoint
#
#
# class MOFArchXLSParserEntryPoint(ParserEntryPoint):
#     """
#     Tandem Parser plugin entry point.
#     """
#
#     def load(self):
#         # lazy import to avoid circular dependencies
#         from nomad_novelmof.parsers.mof_archive_parser import (
#             MOFArchXLSParser,
#         )
#
#         return MOFArchXLSParser(**self.dict())
#
#
# mofarch_xls_parser = MOFArchXLSParserEntryPoint(
#     name='MOFArchXLSParser',
#     description='MOF MOFArch Parser for .xlsx files.',
#     mainfile_name_re=r'.*\.mofarch\.xlsx',
#     # mainfile_content_re='',
#     # mainfile_contents_dict={
#     #     'Master vertical': {
#     #         '__has_all_keys': [
#     #             'Ref. ID temp (Integer starting from 1 and counting upwards)',
#     #         ]
#     #     },
#     # },
# )

class MOFArchJsParserEntryPoint(ParserEntryPoint):
    """
    Tandem Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from nomad_novelmof.parsers.mofarch_json_parser import (
            MOFArchJsParser,
        )

        return MOFArchJsParser(**self.model_dump())


mofarch_json_parser = MOFArchJsParserEntryPoint(
    name='MOFArchJsParser',
    description='MOF MOFArch Parser for Json Files.',
    mainfile_name_re=r'.*\.mofarch\.json',
    # mainfile_content_re='',
    # mainfile_contents_dict={
    #     'Master vertical': {
    #         '__has_all_keys': [
    #             'Ref. ID temp (Integer starting from 1 and counting upwards)',
    #         ]
    #     },
    # },
)
