from ESTRACTER import Estracter_data
import numpy as np
import re
#%%----------------- FUNCIONALIDADES DE VERIFICACION ------------------------------------
## funcionalidad para unificar campos
def UNIQUE_CATEGORIES_SORTED(column):
    strs = column[~column.isnull()]
    strs = strs.unique()
    return sorted(list(strs))  

def Is_not_Number(Serie):
    no_number = []
    for elem in Serie:
        try:
            _ = float(elem)
        except:
            no_number.append(elem)            
    return no_number

def UNIQUE_NO_NUMBERS(Serie):
    return set(Is_not_Number(Serie))  

#----------------------------------------------------------------------------------------
#%%
obj_estracter = Estracter_data('0523.xlsx')
df = obj_estracter.EXTRACT_ALL_DATA_FROM_EXCEL()

#%%
# FUNCIONALIDADES PARA CONVERTIR EN nan's AQUELLOS VALORES QUE DEBERÍAN SERLO
def TO_NAN_FOR_CATEGORY_VARS(column):
    new_column = np.where(
        column == 'None',
        np.nan,
        np.where(
            column == '0',
            np.nan,
            np.where(
                column == '#REF!',
                np.nan,
                np.where(
                    column == '#VALUE!',
                    np.nan,
                    np.where(
                        column == '-',
                        np.nan,
                        column
                        )
                    )
                )
            )  
        )
    return new_column


def TO_NAN_FOR_NUMERIC_VARS(column):
    new_column = np.where(
        column == 'None',
        '0',
        np.where(
            column == '#REF!',
            '0',
            np.where(
                column == '#VALUE!',
                '0',
                np.where(
                    column == '-',
                    '0',
                    column
                    )
                )
            )  
        )
    return new_column


#%%

def CONVERT_SOME_VALUES_IN_NAN(df):
    names_category_vars = list(df.columns[:9]) 
    names_category_vars.append(df.columns[15])
    names_numeric_vars = list(df.columns[9:15])

    for name in names_category_vars:
        df[name] = TO_NAN_FOR_CATEGORY_VARS(df[name])
        
    for name in names_numeric_vars:
        df[name] = TO_NAN_FOR_NUMERIC_VARS(df[name])
        
    return df
        
#%%    
df =  CONVERT_SOME_VALUES_IN_NAN(df)

#%%
def DELETE_NAN_VALUES(df):
    df = df.dropna(thresh=9,ignore_index = True)
    return df

#%%
df_test = DELETE_NAN_VALUES(df)
#%%
fecha_inicio_unique = UNIQUE_CATEGORIES_SORTED(df_test['FECHA INICIO'])
fecha_fin_unique = UNIQUE_CATEGORIES_SORTED(df_test['FECHA FIN'])
#%%
def map_transform_date(date):
    if type(date) == str:
        str_date = date.split()[0]
        try:
            s = re.search('[/]',str_date).group()
            if s == '/':
                new = str_date.split(sep = '/')
                return f'{new[2]}-{new[1]}-{new[0]}'
        except:
            return str_date
    else:
        return date
        
#%%

def TRANSFORM_DATE_COLUMNS(df):
    new_df = df.copy()
    new_df['FECHA INICIO'] = df['FECHA INICIO'].map(map_transform_date)
    new_df['FECHA FIN'] = df['FECHA FIN'].map(map_transform_date)
    return new_df

#%%
df_test = TRANSFORM_DATE_COLUMNS(df_test)


















