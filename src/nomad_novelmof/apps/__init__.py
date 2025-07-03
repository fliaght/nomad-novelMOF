from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import App, Column, Columns, FilterMenu, FilterMenus
from nomad_novelmof.apps.novel_mof_app import novel_mof_app

novel_mof_app_entry_point = AppEntryPoint(
    name='Novel MOF App',
    description='Novel MOF App let you interact with **MOF Archive Data** within NOMAD.',
    app= novel_mof_app
)
