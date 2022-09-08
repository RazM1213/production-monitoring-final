import datetime
import unittest
from datetime import timedelta

import parameterized as parameterized

from config.config import ENV_NAME
from consts.formats import EXACT_TIME_DATE_FORMAT
from models.elastic.elastic_report_response_doc import ReportStat
from models.elastic.error_request_info import ErrorRequestInfo
from models.elastic.status_code_info_doc import StatusCodesInfo
from models.request_info.report_responses import ErrorRequest, ReportResponses
from models.request_info.response_values import ResponseValues
from transform.response.response_transformer import ResponseTransformer


class TestResponseTransformer(unittest.TestCase):
    def test_valid_get_report_responses_one_item_list(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), 200)]

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertEqual(report_responses.request_amount, 1)
        self.assertEqual(report_responses.status_codes, {200: 1})
        self.assertEqual(report_responses.error_requests_info, {})
        self.assertEqual(report_responses.is_failed, False)
        self.assertEqual(report_responses.error_count, 0)
        self.assertEqual(report_responses.request_times, [datetime.timedelta(microseconds=1000)])

    def test_valid_get_report_responses_more_than_one_item_list(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), 200), ResponseValues(timedelta(microseconds=1000), 404)]

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertEqual(report_responses.request_amount, 2)
        self.assertEqual(report_responses.status_codes, {200: 1, 404: 1})
        self.assertEqual(report_responses.is_failed, True)
        self.assertEqual(report_responses.error_count, 1)

    def test_invalid_get_report_responses_empty_list(self):
        # Arrange
        responses_values = []

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertEqual(report_responses, None)

    def test_invalid_get_report_responses_error_contents(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), 404, "Error Test")]

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertEqual(report_responses.error_count, 1)
        self.assertEqual(report_responses.error_requests_info[404][0].content, "Error Test")
        self.assertEqual(report_responses.is_failed, True)

    def test_invalid_get_report_responses_no_status_codes(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000))]

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertEqual(report_responses, None)

    @parameterized.parameterized.expand([
        (300,),
        (400,),
        (500,)
    ])
    def test_invalid_get_report_responses_non_success_status_code(self, status_code):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), status_code)]

        # Act
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Assert
        self.assertIsInstance(report_responses.error_requests_info[status_code][0], ErrorRequest)

    def test_valid_get_elastic_report_doc_default_report_responses(self):
        # Arrange
        report_responses = ReportResponses(request_amount=1)
        route_name = "Test"

        # Act
        elastic_report_response_doc = ResponseTransformer.get_elastic_report_doc(route_name=route_name, report_responses=report_responses)

        # Assert
        self.assertEqual(elastic_report_response_doc.name, route_name)
        self.assertIsInstance(datetime.datetime.strptime(elastic_report_response_doc.time, EXACT_TIME_DATE_FORMAT), datetime.datetime)
        self.assertIsInstance(elastic_report_response_doc.status_code_info, StatusCodesInfo)
        self.assertIsInstance(elastic_report_response_doc.report_stat, ReportStat)
        self.assertEqual(elastic_report_response_doc.run_stat, ENV_NAME)

    def test_valid_get_elastic_report_doc_success_status_codes_info(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), 200)]
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)
        route_name = "Test"

        # Act
        elastic_report_response_doc = ResponseTransformer.get_elastic_report_doc(route_name=route_name, report_responses=report_responses)

        # Assert
        self.assertEqual(elastic_report_response_doc.name, route_name)
        self.assertEqual(elastic_report_response_doc.status_code_info.status_codes_counter[0].status_code, 200)
        self.assertEqual(elastic_report_response_doc.status_code_info.status_codes_counter[0].count, 1)
        self.assertEqual(elastic_report_response_doc.status_code_info.error_requests_info, [])
        self.assertEqual(elastic_report_response_doc.status_code_info.is_failed, False)
        self.assertEqual(elastic_report_response_doc.status_code_info.error_count, 0)

    def test_valid_get_elastic_report_doc_non_success_status_codes_info(self):
        # Arrange
        responses_values = [ResponseValues(timedelta(microseconds=1000), 400)]
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)
        route_name = "Test"

        # Act
        elastic_report_response_doc = ResponseTransformer.get_elastic_report_doc(route_name=route_name, report_responses=report_responses)

        # Assert
        self.assertEqual(elastic_report_response_doc.status_code_info.status_codes_counter[0].status_code, 400)
        self.assertEqual(elastic_report_response_doc.status_code_info.status_codes_counter[0].count, 1)
        self.assertIsInstance(elastic_report_response_doc.status_code_info.error_requests_info[0], ErrorRequestInfo)
        self.assertEqual(elastic_report_response_doc.status_code_info.is_failed, True)
        self.assertEqual(elastic_report_response_doc.status_code_info.error_count, 1)

    def test_valid_default_get_request_time(self):
        # Arrange
        responses_values = [
            ResponseValues(timedelta(microseconds=1000), 200),
            ResponseValues(timedelta(microseconds=2000), 400),
            ResponseValues(timedelta(microseconds=3000), 500)
        ]
        report_responses = ResponseTransformer.get_report_responses(responses_values=responses_values)

        # Act
        request_time = ResponseTransformer.get_request_time(report_responses)

        # Assert
        self.assertEqual(request_time.average, 0.002)
        self.assertEqual(request_time.minimum, 0.001)
        self.assertEqual(request_time.maximum, 0.003)

