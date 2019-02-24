import pytest

from serverless_hello.worker_support import eval_expression


def test_eval_expression():
    assert(eval_expression('1+2+3') == '6')


