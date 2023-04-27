from ...services.elastic.dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()

from ...services.elastic import request
from ._RequestCtrl import _RequestCtrl

# from ...schema.base.entities._Corpus import NER_Corpus
from ...schema.ai.Corpus import NER_Corpus, DRUG_Corpus
from ...schema.base.entities._Doc import _Doc
from ...services import i2b2 as i2b2_svc
from ...services import n2c2 as n2c2_svc

# from ...schema.base.messages._MessageEnums import MsgEntity


class CorpusCtrl(_RequestCtrl):
    @classmethod
    async def search_documents(self, index, req, es=_es):
        _res = await request.search_documents("doc", req.query, es)
        if req.msg_entity_type == "deID":
            # 1. get internal docs
            _docs = [_Doc(**doc) for doc in _res]
            ner_docs = await NER_Corpus.convert_docs(_docs)
            _corpus = NER_Corpus(docs=ner_docs)
            # 2. get external docs
            train = await i2b2_svc.get_i2b2("train")
            test = await i2b2_svc.get_i2b2("test")
            i2b2_docs = train[0]["docs"] + test[0]["docs"]

            _corpus.add_docs(i2b2_docs)

            return [_corpus]
        elif req.msg_entity_type == "drug":
            # 1. get internal docs
            # TODO: not handling internal docs at all yet
            # _docs = [_Doc(**doc) for doc in _res]
            # ner_docs = await DRUG_Corpus.convert_docs(_docs)
            # _corpus = DRUG_Corpus(docs=ner_docs)

            # 2. get external docs
            docs_by_label = {}

            labels = req.data["labels"]

            for label in labels:
                n2c2_docs = await n2c2_svc.get_n2c2([label])
                if len(n2c2_docs) > 0:
                    docs_by_label[label] = DRUG_Corpus(docs=n2c2_docs[0]["docs"])

            return [{"docs": docs_by_label, "uuid": req.uuid}]

        return _res
