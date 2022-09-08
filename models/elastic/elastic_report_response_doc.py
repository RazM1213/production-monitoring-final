from dataclasses import dataclass
from uuid import uuid4

from models.elastic.request_time import RequestTime
from models.elastic.status_code_info_doc import StatusCodesInfo


@dataclass
class ReportStat:
    request_time: RequestTime = RequestTime()
    request_amount: int = 0


@dataclass
class RunStat:
    env: str
    request_time: RequestTime = RequestTime()
    amount: int = 0


@dataclass
class ElasticReportResponseDoc:
    name: str
    time: str
    status_code_info: StatusCodesInfo
    report_stat: ReportStat
    run_stat: RunStat
    id: str = str(uuid4())
