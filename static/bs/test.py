import pandas as pd

data_path = f"классификатор СП.xlsx"  # файл с указанием названий филиалов Неисправности или отклонения  от норм содержания (группы)
get_data = pd.read_excel(data_path)

# for x in get_data['Объекты осмотра'].unique():
#     print(x)
# input()
# res = (get_data.groupby(['Объекты осмотра',
#                          'Осматриваемые элементы и характеристики',
#                          'Неисправности или отклонения  от норм содержания (группы)',
#                          'Неисправности или отклонения  от норм содержания (виды)'])
#        [['Интервал отклонения', 'Интервал отклонения2', 'Крайний срок (в днях)', 'Единица измерения', 'Ограничение скорости']]
#        .apply(lambda x: list(x.values))
#        .reset_index(name='info'))
# # print(res)
# for idx_data_sp in res.index:
#     print(res['Объекты осмотра'][idx_data_sp],
#           ' -> ',
#           res['Осматриваемые элементы и характеристики'][idx_data_sp].replace('  ', ' '),
#           ' => ',
#           res['Неисправности или отклонения  от норм содержания (группы)'][idx_data_sp],
#           ' => ',
#           res['Неисправности или отклонения  от норм содержания (виды)'][idx_data_sp],
#           ' => ',
#           res['info'][idx_data_sp][0]
#           )

get_data = get_data.fillna('-')

count = 1
for idx_data_sp in get_data.index:
    print(count, ' : ', get_data['Объекты осмотра'][idx_data_sp], ' -> ',
          get_data['Осматриваемые элементы и характеристики'][idx_data_sp].replace('  ', ' '), ' => ',
          get_data['Неисправности или отклонения  от норм содержания (группы)'][idx_data_sp], ' => ',
          get_data['Неисправности или отклонения  от норм содержания (виды)'][idx_data_sp], ' => ',
          get_data['Интервал отклонения'][idx_data_sp],get_data['Интервал отклонения2'][idx_data_sp],get_data['Крайний срок (в днях)'][idx_data_sp],get_data['Единица измерения'][idx_data_sp],get_data['Ограничение скорости'][idx_data_sp]
          )

    count += 1
