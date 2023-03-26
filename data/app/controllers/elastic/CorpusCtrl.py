from ...services.elastic.dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()

from ...services.elastic import request
from ._RequestCtrl import _RequestCtrl

# from ...schema.base.entities._Corpus import NER_Corpus
from ...schema.ai.Corpus import NER_Corpus
from ...schema.base.entities._Doc import _Doc
from ...services import i2b2 as i2b2_svc

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
        return _res
