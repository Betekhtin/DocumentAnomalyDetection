from collections import defaultdict

from natasha import Combinator, DEFAULT_GRAMMARS

from ContractStructure import Document

DG_INTERP = {'<enum \'Money\'>': 'Деньги',
             '<enum \'Person\'>': 'Личность',
             '<enum \'Location\'>': 'Место',
             '<enum \'Street\'>': 'Улица',
             '<enum \'Address\'>': 'Адрес',
             '<enum \'Date\'>': 'Дата',
             '<enum \'Brand\'>': 'Брэнд',
             '<enum \'Event\'>': 'Событие',
             '<enum \'Organisation\'>': 'Организация'}


def __extract_entities(sent_obj):
    entities = defaultdict(list)
    sent = sent_obj.sentence

    grammar = DEFAULT_GRAMMARS
    combinator = Combinator(grammar)

    matches = combinator.resolve_matches(
        combinator.extract(sent),
    )
    for j, m in matches:
        name = DG_INTERP[str(type(j))]
        start = m[0].position[0]
        end = m[-1].position[1]
        entities[name].append((start, end))
    return entities


def __mark_positions(par):
    """
    Walks `Paragraph` object as a tree.
    Starting from the leafs, every `Sentence` object updates information about `named_entities`.
    :par: `Paragraph` object.
    """
    if par.children:
        for child in par.children:
            __mark_positions(child)
    for sent in par.sentences:
        print(sent)
        sent.named_entities = __extract_entities(sent)


def extract(doc: Document):
    """
    Walks `Document` as a tree and updates field `named_entities` in `Sentences`
    """
    #    marked_doc = doc.copy()
    #    map(__mark_positions, doc.main_text)
    for ch in doc.main_text:
        __mark_positions(ch)
    __mark_positions(doc.preamble)
    __mark_positions(doc.attachment)
    return doc


if __name__ == "__main__":
    doc = Document('/tmp/a.doc')
    doc = extract(doc)
    print(doc)
