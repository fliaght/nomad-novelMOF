from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Layout,
    Markers,
    SearchQuantities,
    WidgetHistogram,
    WidgetPeriodicTable,
    WidgetScatterPlot,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuItemPeriodicTable,
    MenuSizeEnum,
    WidgetTerms
)

SCHEMA = "nomad_novelmof.schema_packages.novelmof_mofarch.MOFArchive"

novel_mof_app = App(
        # ------------------------------------------------ overview ----------
        label="MOF Archive Database",
        path="mofarchivedb",
        category="Use Cases",
        description=(
            "Curated structural and synthesis information from literature."
        ),
        readme=(
            '''
            Novel MOF App let you interact with **MOF Archive Data** within NOMAD.
        The filter menu on the left and the shown
        default columns are specifically designed for Heterogeneous Catalyst
        exploration. The dashboard directly shows useful
        interactive statistics about the data.\n'''
        ),

        # # ---------------------------- search index -------------------------

        # 不加这个参数全局崩溃。。。。
        search_quantities=SearchQuantities(include=[f"*#{SCHEMA}"]),

        # ---------------------------- fixed filters ------------------------
        filters_locked={"section_defs.definition_qualified_name": [SCHEMA]},

        # ---------------------------- result table -------------------------
        # 还记得右边dashboard下面显示条目的表格吗？这里定义了表格的列
        columns=[
            Column(
                search_quantity=f"data.identifier#{SCHEMA}",
                label="MOF Identifier",
                selected=True,
            ),
            Column(
                search_quantity=f"data.common_name#{SCHEMA}",
                label="Common MOF Name",
                selected=True,
            ),
            Column(
                search_quantity=f"data.calculation_properties.structural_properties.pore_characteristics.PLD_angstrom#{SCHEMA}",
                label="Pore Diameter (PLD)",
                unit= 'angstrom',
                selected=True,
            ),
            Column(
                search_quantity=f"data.calculation_properties.structural_properties.topological_and_crystallographic_information.hall#{SCHEMA}",
                label="Hall Symbol",
                selected=True,
            ),
            Column(
                search_quantity=f"data.reference_data.year#{SCHEMA}",
                label="Publication Year",
                selected=True,
            )
        ],

        # ------------------------------ menu -----------------------------
        menu=Menu(
            title="Archive Filters",
            items=[

                Menu(
                    title='Publication',
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemTerms(
                            search_quantity=f'data.reference_data.doi#{SCHEMA}',
                            show_input=True,
                            options=10,
                            title='DOI',
                        ),
                        # MenuItemTerms(
                        #     search_quantity=f'data.reference_data.year#{SCHEMA}',
                        #     title='Publication Year',
                        #     show_input=False,
                        #     options=10,
                        # ),
                    ],
                ),
                Menu(
                    title='Compositiional Properties',
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemPeriodicTable(
                            search_quantity='results.material.elements'
                        ),
                    ],
                ),
                Menu(
                    title='Synthesis Information',
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemTerms(
                            search_quantity=f"data.synthesis_information.synthesis_method#{SCHEMA}",
                            show_input=True,
                            width=6,
                            options=10,
                            title="Synthesis Method",
                        ),
                    ],
                ),
                # Menu(
                #     title='Structural Properties',
                #     size=MenuSizeEnum.XXL,
                #     items=[
                #         MenuItemTerms(
                #             search_quantity=f"data.calculation_properties.structural_properties.topological_and_crystallographic_information.topology_single_nodes#{SCHEMA}",
                #             title='Topology by Single Nodes',
                #         ),
                #         MenuItemTerms(
                #             search_quantity=f"data.calculation_properties.structural_properties.topological_and_crystallographic_information.number_spacegroup#{SCHEMA}",
                #             title='Space Group Number',
                #         ),
                #     ],
                # )



                # categorical ­––––––––––––––––––––––––––––––––––––––––––––


                # # numerical ­–––––––––––––––––––––––––––––––––––––––––––––––
                # MenuItemHistogram(
                #     x=Axis(
                #         search_quantity=f"data.Material_entries.capacity#{SCHEMA}",
                #         title="Capacity",
                #     ),
                # ),
                # MenuItemHistogram(
                #     x=Axis(
                #         search_quantity=f"data.Material_entries.voltage#{SCHEMA}",
                #         title="Voltage",
                #     ),
                # ),
            ],
        ),

        # ---------------------------- dashboard ----------------------------
        dashboard=Dashboard(
            widgets=[
                # --- periodic table (unchanged) ---
                WidgetPeriodicTable(
                    layout={
                        'lg': Layout(h=8, minH=8, minW=12, w=12, x=0, y=0), # total w = 24
                        'md': Layout(h=8, minH=8, minW=10, w=10, x=0, y=0), # total w = 18
                    },
                    search_quantity='results.material.elements',
                    scale='linear',
                    title='Elements of the MOF material',
                ),

                WidgetHistogram(
                    title="Pore Diameter (PLD)",
                    x=f"data.calculation_properties.structural_properties.pore_characteristics.PLD_angstrom#{SCHEMA}",
                    n_bins=100,
                    autorange=True,
                    showinput=False,
                    layout={
                        'lg': Layout(h=4, minH=4, minW=12, w=12, x=12, y=0),
                        'md': Layout(h=4, minH=4, minW=8, w=8, x=10, y=0),
                    }
                ),
                WidgetHistogram(
                    title="Synthesis Temperature",
                    x=f"data.synthesis_information.synthesis_parameter.temperature#{SCHEMA}",
                    n_bins=100,
                    autorange=True,
                    showinput=False,
                    layout={
                        'lg': Layout(h=4, minH=4, minW=12, w=12, x=12, y=4),
                        'md': Layout(h=4, minH=4, minW=8, w=8, x=10, y=4),
                    }
                ),
                WidgetTerms(
                    title='hall symbol',
                    layout={
                        'lg': Layout(h=8, minH=8, minW=6, w=6, x=0, y=8),
                        'md': Layout(h=8, minH=8, minW=4, w=4, x=0, y=8),
                    },
                    search_quantity=f'data.calculation_properties.structural_properties.topological_and_crystallographic_information.hall#{SCHEMA}',
                ),
                WidgetTerms(
                    title='Publisher',
                    layout={
                        'lg': Layout(h=8, minH=8, minW=6, w=6, x=6, y=8),
                        'md': Layout(h=8, minH=8, minW=4, w=4, x=4, y=8),
                    },
                    search_quantity=f'data.reference_data.publication#{SCHEMA}',
                ),

                WidgetHistogram(
                    title="ASA (m2/cm3)",
                    x=f"data.calculation_properties.structural_properties.pore_characteristics.ASA_m2_cm3#{SCHEMA}",
                    n_bins=100,
                    autorange=True,
                    showinput=False,
                    layout={
                        'lg': Layout(h=4, minH=4, minW=12, w=12, x=12, y=8),
                        'md': Layout(h=4, minH=4, minW=10, w=10, x=8, y=8),
                    }
                ),
                WidgetHistogram(
                    title="Pore Volume (PV) (cm3/g)",
                    x=f"data.calculation_properties.structural_properties.pore_characteristics.PV_cm3_g#{SCHEMA}",
                    n_bins=100,
                    autorange=True,
                    showinput=False,
                    layout={
                        'lg': Layout(h=4, minH=4, minW=12, w=12, x=12, y=12),
                        'md': Layout(h=4, minH=4, minW=10, w=10, x=8, y=12),
                    }
                ),

                # --- scatter plot (Voltage vs Capacity coloured by Specifier) --
                # WidgetScatterPlot(
                #     title="Time vs Temperature",
                #     x=Axis(
                #         search_quantity=f"data.synthesis_information.synthesis_parameter.temperature#{SCHEMA}",
                #         title="Temperature (Celsius)",
                #     ),
                #     y=Axis(
                #         search_quantity=f"data.synthesis_information.synthesis_parameter.time#{SCHEMA}",
                #         title="Time (hours)",
                #     ),
                #     markers=Markers(
                #         color=Axis(
                #             search_quantity=f"data.synthesis_information.synthesis_method#{SCHEMA}",
                #             title="Synthesis Method",
                #         )
                #     ),
                #     size=800,
                #     autorange=True,
                #     layout={"lg": Layout(w=6, h=8, x=12, y=0, minW=6, minH=6)},
                # ),
            ],
        ),
    )

# 当你使用 from module import * 时，Python 默认会导入模块中所有不以下划线 _ 开头的名称（除非它们被定义在函数或类的局部作用域内）。

# 然而，__all__ 变量提供了一种明确控制这种行为的方式。如果一个模块定义了 __all__ 列表，那么 from module import * 就只会导入 __all__ 列表中列出的名称，而忽略其他所有公共名称。
__all__ = ["novel_mof_app"]
