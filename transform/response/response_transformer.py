from datetime import datetime
from typing import List

from config.config import ENV_NAME
from consts.formats import EXACT_TIME_DATE_FORMAT
from models.elastic.elastic_report_response_doc import ElasticReportResponseDoc, ReportStat
from models.elastic.error_request_info import ErrorRequestInfo, OrderPositionDetails
from models.elastic.request_time import RequestTime
from models.elastic.status_code_counter import StatusCodeCounter
from models.elastic.status_code_info_doc import StatusCodesInfo
from models.request_info.report_responses import ReportResponses, ErrorRequest
from models.request_info.response_values import ResponseValues


class ResponseTransformer:
    @staticmethod
    def get_report_responses(responses_values: List[ResponseValues]) -> ReportResponses:
        report_responses = ReportResponses(request_amount=len(responses_values))
        if report_responses.request_amount == 0:
            return None

        for response_values in responses_values:
            if response_values.status_code is None:
                return None

        response_values_index = 0
        for response_values in responses_values:
            if response_values.status_code in report_responses.status_codes:
                report_responses.status_codes[response_values.status_code] += 1
            else:
                report_responses.status_codes[response_values.status_code] = 1
                if response_values.status_code // 100 != 2:
                    report_responses.error_requests_info[response_values.status_code] = []

            if response_values.status_code // 100 != 2:
                report_responses.error_requests_info[response_values.status_code].append(ErrorRequest(response_values_index, response_values.error_content))
                report_responses.error_count += 1
                report_responses.is_failed = True

            report_responses.request_times.append(response_values.time)

            response_values_index += 1

        return report_responses

    @staticmethod
    def get_elastic_report_doc(route_name: str, report_responses: ReportResponses) -> ElasticReportResponseDoc:
        status_codes_info: List[StatusCodeCounter] = []
        for status_code in report_responses.status_codes:
            # if len(ResponseTransformer.get_status_code_info(status_codes_info, status_code)) != 0:
            #     ResponseTransformer.get_status_code_info(status_codes_info, status_code)[0].count += report_responses.status_codes[status_code]
            # else:
            status_codes_info.append(StatusCodeCounter(status_code, report_responses.status_codes[status_code]))

        error_requests_info: List[ErrorRequestInfo] = []
        error_index = 0
        for error_status_code in report_responses.error_requests_info:
            error_requests_info.append(ErrorRequestInfo(error_status_code, []))
            for error_request_info in report_responses.error_requests_info.get(error_status_code):
                error_requests_info[error_index].order_positions.append(OrderPositionDetails(error_request_info.position, error_request_info.content))

            error_index += 1

        return ElasticReportResponseDoc(
            name=route_name,
            time=datetime.now().strftime(EXACT_TIME_DATE_FORMAT)[:-3],
            status_code_info=StatusCodesInfo(status_codes_info, error_requests_info, report_responses.is_failed, report_responses.error_count),
            report_stat=ReportStat(ResponseTransformer.get_request_time(report_responses), len(report_responses.request_times)),
            run_stat=ENV_NAME
        )

    # @staticmethod
    # def get_status_code_info(status_code_list: List[StatusCodeCounter], status_code: int) -> [List[StatusCodeCounter]]:
    #     return list(filter(lambda status: status.status_code == status_code, status_code_list))

    @staticmethod
    def get_request_time(responses: ReportResponses) -> RequestTime:
        request_times = list(map(lambda time: time.total_seconds(), responses.request_times))
        if len(request_times) != 0:
            return RequestTime(sum(request_times) / len(request_times), max(request_times), min(request_times))
        return RequestTime()
