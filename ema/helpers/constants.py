"""Constants for the project."""
from os import getcwd, path
from os.path import join

PATH = path.abspath(getcwd())
DATA = join(PATH, 'data')
WORKSPACE = join(PATH, 'workspace')
DATA_RAW = join(DATA, 'raw')
DATA_RAW_JSONS = join(DATA_RAW, 'jsons')
DATA_RAW_IMAGES = join(DATA_RAW, 'images')
DATA_INTERIM = join(DATA, 'interim')
DATA_INTERIM_TEXT = join(DATA_INTERIM, 'jsons')
DATA_INTERIM_IMAGES = join(DATA_INTERIM, 'images')
DATA_PROCD = join(DATA, 'processed')
DATA_PROCD_TEXT = join(DATA_PROCD, 'jsons')
DATA_PROCD_IMAGES = join(DATA_PROCD, 'images')
DATA_PROCD_MODEL = join(DATA_PROCD, 'modeldb')

TESAURO = ['05']

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}


MUSEUM_DICT = {
        "MINC": "https://museudainconfidencia.acervos.museus.gov.br/wp-json/tainacan/v2/collection/9/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MRCO": "https://museuregionalcasadosottoni.acervos.museus.gov.br/wp-json/tainacan/v2/collection/31492/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MVLL": "https://museuvillalobos.acervos.museus.gov.br/wp-json/tainacan/v2/collection/1570/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MCHE": "http://museucasadahera.acervos.museus.gov.br/wp-json/tainacan/v2/collection/7/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MARI": "https://museudearqueologiadeitaipu.museus.gov.br/wp-json/tainacan/v2/collection/94553/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MCPR": "https://museusibramgoias.acervos.museus.gov.br/wp-json/tainacan/v2/collection/1227/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MCBC": "https://museucasabenjaminconstant.acervos.museus.gov.br/wp-json/tainacan/v2/collection/5347/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MDIA": "https://museudodiamante.acervos.museus.gov.br/wp-json/tainacan/v2/collection/11603/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MASB": "https://museusibramgoias.acervos.museus.gov.br/wp-json/tainacan/v2/collection/3387/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MHNA": "https://mhn.acervos.museus.gov.br/wp-json/tainacan/v2/collection/24/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MCHA": "http://museucasahistoricadealcantara.acervos.museus.gov.br/wp-json/tainacan/v2/collection/14284/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MBAN": "https://museusibramgoias.acervos.museus.gov.br/wp-json/tainacan/v2/collection/1093/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MRSJ": "https://museuregionaldesaojoaodelrei.acervos.museus.gov.br/wp-json/tainacan/v2/collection/11451/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MVIM": "https://museuvictormeirelles.acervos.museus.gov.br/wp-json/tainacan/v2/collection/18004/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MOUR": "https://museudoouro.acervos.museus.gov.br/wp-json/tainacan/v2/collection/3583/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MMIS": "https://museudasmissoes.acervos.museus.gov.br/wp-json/tainacan/v2/collection/6409/items/?perpage=96&order=DESC&orderby=date&paged=",
        "MABO": "https://museudaabolicao.acervos.museus.gov.br/wp-json/tainacan/v2/collection/7/items/?perpage=96&order=DESC&orderby=date&paged="
        }

ACRONYN = {
        'MINC',
        'MRCO',
        'MVLL',
        'MCHE',
        'MARI',
        'MCPR',
        'MCBC',
        'MDIA',
        'MASB',
        'MHNA',
        'MCHA',
        'MBAN',
        'MRSJ',
        'MVIM',
        'MOUR',
        'MMIS',
        'MABO'
        }

# Museu Regional Casa dos Ottoni
MRCO_ACR = 'MRCO'
MRCO_FIELDS = {
        'classification': ['metadata', 'classificacao-2', 'value_as_string'],
        'denomination': ['metadata', 'denominacao', 'value_as_string'],
        'title': ['title']
        }

# Museu da Inconfidência
MINC_ACR = 'MINC'
MINC_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title', 'value_as_string'],
        'title': ['title']
        }

# Museu Villa Lobos
MVLL_ACR = 'MVLL'
MVLL_FIELDS = {
        'classification': ['metadata', 'classe',  'value_as_string'],
        'denomination': ['metadata', 'denominacao', 'value_as_string'],
        'title': ['title']
        }

# Museu Casa da Hera
MCHE_ACR = 'MCHE'
MCHE_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title', 'value_as_string'],
        'title': ['title']
        }

# Museu de Arqueologia de Itaipu
MARI_ACR = 'MARI'
MARI_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title-28', 'value_as_string'],
        'title': ['title']
        }

# Museu Casa da Princesa
MCPR_ACR = 'MCPR'
MCPR_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title-2', 'value_as_string'],
        'title': 'title'
        }

# Museu Casa Benjamin Constant
MCBC_ACR = 'MCBC'
MCBC_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title-4', 'value_as_string'],
        'title': ['title']
        }

# Museu do Diamante
MDIA_ACR = 'MDIA'
MDIA_FIELDS = {
        'classification': ['metadata', 'classe-3', 'value_as_string'],
        'denomination': ['metadata', 'title-3', 'value_as_string'],
        'title': ['title']
        }

# Museu de Arte Sacra da Boa Morte
MASB_ACR = 'MASB'
MASB_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title-3', 'value_as_string'],
        'title': ['title']
        }


# Museu Histórico Nacional
MHNA_ACR = 'MHNA'
MHNA_INTERIOR = 'metadata.classe-2.value_as_string'
MHNA_FIELDS = {
        'classification': ['metadata', 'classe-2', 'value_as_string'],
        'denomination': ['metadata', 'title', 'value_as_string'],
        'title': ['title']
        }

# Museu Casa Histórica de Alcântara
MCHA_ACR = 'MCHA'
MCHA_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title-4', 'value_as_string'],
        'title': ['title']
        }

# Museu da Bandeiras
MBAN_ACR = 'MBAN'
MBAN_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'title', 'value_as_string'],
        'title': ['title']
        }

# Museu Regional de São João Del Rei
MRSJ_ACR = 'MRSJ'
MRSJ_FIELDS = {
        'classification': ['metadata', 'classificacao-2', 'value_as_string'],
        'denomination': ['metadata', 'title-3', 'value_as_string'],
        'title': ['title']
        }

# Museu Victor Meirelles
MVIM_ACR = 'MVIM'
MVIM_FIELDS = {
        'classification': ['metadata', 'taxonomia', 'value_as_string'],
        'denomination': ['metadata', 'objeto-2', 'value_as_string'],
        'title': ['title']
        }

# Museu do Ouro
MOUR_ACR = 'MOUR'
MOUR_FIELDS = {
        'classification': ['metadata', 'classificacao-3', 'value_as_string'],
        'denomination': ['metadata', 'title-4', 'value_as_string'],
        'title': ['title']
        }

# Museu das Missões
MMIS_ACR = 'MMIS'
MMIS_FIELDS = {
        'classification': ['metadata', 'classificacao', 'value_as_string'],
        'denomination': ['metadata', 'denominacao', 'value_as_string'],
        'title': ['title']
        }

# Museu da Abolição
MABO_ACR = 'MABO'
MABO_FIELDS = {
        'classification': ['metadata', 'classificacao-thesauros-1987', 'value_as_string'],
        'denomination': ['metadata', 'objeto-nome', 'value_as_string'],
        'title': ['title']
        }

TARGET_LABELS = [
    'prato',
    'cadeira',
    'mesa',
    'oratório',
    'castiçal',
    'arandela',
    'colher',
    'talher',
    'luminária',
    'garfo',
    'faca',
    'cortina',
    'espelho',
    'xícara',
    'aparador',
    'arca',
    'armário',
    'travessa',
    'pires',
    'leito',
    'taça',
    'copo',
    'garrafa',
    'lustre',
    'panela',
    'jarra',
    'lanterna',
    'cômoda',
    'vaso',
    'candeia',
    'lampião'
]

EN_TARGET_LABELS = [
    'dish',
    'chair',
    'table',
    'oratory',
    'candlestick',
    'sconce',
    'spoon',
    'cutlery ',
    'luminaire',
    'fork',
    'table knife',
    'curtain',
    'mirror',
    'cup of tea',
    'sideboard',
    'chest',
    'wardrobe',
    'platter',
    'saucer',
    'bed',
    'glass',
    'cup',
    'bottle',
    'chandelier',
    'pan',
    'jug',
    'lantern',
    'chest of drawers',
    'vase',
    'lamp',
    'keerosene lamp'
]

# target labels in portuguese and english
TL_JOINED = [
    ('prato', 'dish'),
    ('cadeira', 'chair'),
    ('mesa', 'table'),
    ('oratório', 'oratory'),
    ('castiçal', 'candlestick'),
    ('arandela', 'sconce'),
    ('colher', 'spoon'),
    ('talher', 'cutlery'),
    ('luminária', 'luminaire'),
    ('garfo', 'fork'),
    ('faca', 'table knife'),
    ('cortina', 'curtain'),
    ('espelho', 'mirror'),
    ('xícara', 'cup of tea'),
    ('aparador', 'sideboard'),
    ('arca', 'chest'),
    ('armário', 'wardrobe'),
    ('travessa', 'platter'),
    ('pires', 'saucer'),
    ('leito', 'bed'),
    ('taça', 'glass'),
    ('copo', 'cup'),
    ('garrafa', 'bottle'),
    ('lustre', 'chandelier'),
    ('panela', 'pan'),
    ('jarra', 'jug'),
    ('lanterna', 'lantern'),
    ('cômoda', 'chest of drawers'),
    ('vaso', 'vase'),
    ('candeia', 'lamp'),
    ('lampião', 'keerosene lamp')
]

TL_BW = {
    'prato': ['prato decorativo'],
    'cadeira': [],
    'mesa': [
        'toalha de mesa',
        'sobremesa',
        'pano de mesa',
        'garfo de mesa',
        'pote (cozinha/mesa)',
        'faca de mesa'],
    'oratório': [],
    'castiçal': [],
    'arandela': [],
    'colher': [],
    'talher': [],
    'luminária': [],
    'garfo': [],
    'faca': [],
    'cortina': ['aparador de cortina'],
    'espelho': [],
    'xícara': [],
    'aparador': ['aparador de cortina'],
    'arca': [],
    'armário': [],
    'travessa': [],
    'pires': [],
    'leito': [],
    'taça': [],
    'copo': [],
    'garrafa': [],
    'lustre': [],
    'panela': [],
    'jarra': [],
    'lanterna': [],
    'cômoda': [],
    'vaso': [],
    'candeia': [],
    'lampião': []
}
