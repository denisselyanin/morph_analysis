from morph_analysis import parse_sentence
from plot_decomposition import  plot_decomposition

all_tests = [
    "пожарить 15 вкусных сырников",
    "Веселые дети купили белые и синие шарики",
    "Комиссия руководствуется международными академическими стандартами в проведении исследований",
    "Федеральный портал проектов нормативных правовых актов — официальный сайт для размещения информации о подготовке проектов нормативных правовых актов",
    "Отменить приказ, утративший всякую силу, сегодня",
    "Прием проводится отдельно для обучения в Университете и для обучения в филиалах Университета"
]

do_plot = True

for sentence in all_tests:
    parsed = parse_sentence(sentence)
    assert len(parsed) > 0
    if do_plot:
        for p in parsed:
            plot_decomposition(sentence, p[1])

