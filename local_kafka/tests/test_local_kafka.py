# -*- coding: utf-8 -*-
from unittest.mock import Mock
from app.app import App
import os
import pytest
from json import dumps


class TestTopology:
    @classmethod
    def setup_class(self):
        os.environ["INPUT_TOPIC_NAME"] = "test-input-topic"
        os.environ["OUTPUT_TOPIC_NAME"] = "test-output-topic"
        os.environ["BOOTSTRAP_SERVER"] = "localhost:9093"
        self.app = App()
        self.app.consumer = Mock()
        self.app.producer = Mock()
        self.app.producer.send = Mock()

    @pytest.mark.parametrize(
        "timestamp, expected_utc",
        [
            ("2022-05-06T14:30:00+00:00", "2022-05-06T14:30:00+00:00"),
            ("2022-05-06T14:30:00+01:00", "2022-05-06T13:30:00+00:00"),
        ],
    )
    def test_topology_utc_conversion(self, timestamp, expected_utc):

        valid_timestamp_record = {
            "myKey": "123",
            "myTimestamp": timestamp,
        }

        valid_timestamp_msg = Mock()
        valid_timestamp_msg.value = dumps(valid_timestamp_record)

        self.app.consumer = [valid_timestamp_msg]
        self.app.topology()

        expected_record = {
            "myKey": "123",
            "myTimestamp": expected_utc,
        }

        _, kwargs = self.app.producer.send.call_args

        assert kwargs.get("key") == "123"
        assert kwargs.get("value") == expected_record

    def test_topology_empty_timestamp(self):

        valid_timestamp_record = {
            "myKey": "123",
            "myTimestamp": "",
        }

        valid_timestamp_msg = Mock()
        valid_timestamp_msg.value = dumps(valid_timestamp_record)

        self.app.consumer = [valid_timestamp_msg]
        self.app.topology()

        expected_record = {
            "myKey": "123",
            "myTimestamp": "",
        }

        _, kwargs = self.app.producer.send.call_args

        assert kwargs.get("key") == "123"
        assert kwargs.get("value") == expected_record

    def test_topology_no_timestamp(self):

        valid_timestamp_record = {"myKey": "123"}

        valid_timestamp_msg = Mock()
        valid_timestamp_msg.value = dumps(valid_timestamp_record)

        self.app.consumer = [valid_timestamp_msg]
        self.app.topology()

        expected_record = {"myKey": "123"}

        _, kwargs = self.app.producer.send.call_args

        assert kwargs.get("key") == "123"
        assert kwargs.get("value") == expected_record

    def test_topology_invalid_timestamp(self):

        self.app.producer.send = Mock()
        invalid_timestamp_record = {
            "myKey": "456",
            "myTimestamp": "2022-05-06T24:00:00+00:00",
        }

        invalid_timestamp_msg = Mock()
        invalid_timestamp_msg.value = dumps(invalid_timestamp_record)

        self.app.consumer = [invalid_timestamp_msg]
        self.app.topology()

        self.app.producer.send.assert_not_called()
