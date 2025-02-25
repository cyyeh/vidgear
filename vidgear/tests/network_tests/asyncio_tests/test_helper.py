"""
===============================================
vidgear library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2019-2020 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
"""
# import the necessary packages

import sys
import numpy as np
import pytest
import logging as log

from vidgear.gears.asyncio.helper import reducer, create_blank_frame, logger_handler

# define test logger
logger = log.getLogger("Test_Asyncio_Helper")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(log.DEBUG)


def getframe():
    """
    returns empty numpy frame/array of dimensions: (500,800,3)
    """
    return (np.random.standard_normal([500, 800, 3]) * 255).astype(np.uint8)


pytestmark = pytest.mark.asyncio


@pytest.mark.skipif(
    sys.version_info >= (3, 8),
    reason="python3.8 is not supported yet by pytest-asyncio",
)
@pytest.mark.parametrize(
    "frame , percentage, result",
    [(getframe(), 85, True), (None, 80, False), (getframe(), 95, False)],
)
async def test_reducer_asyncio(frame, percentage, result):
    """
    Testing frame size reducer function
    """
    if not (frame is None):
        org_size = frame.shape[:2]
    try:
        reduced_frame = await reducer(frame, percentage)
        logger.debug(reduced_frame.shape)
        assert not (reduced_frame is None)
        reduced_frame_size = reduced_frame.shape[:2]
        assert (
            100 * reduced_frame_size[0] // (100 - percentage) == org_size[0]
        )  # cross-check width
        assert (
            100 * reduced_frame_size[1] // (100 - percentage) == org_size[1]
        )  # cross-check height
    except Exception as e:
        if isinstance(e, ValueError) and not (result):
            pass
        else:
            pytest.fail(str(e))


@pytest.mark.skipif(
    sys.version_info >= (3, 8),
    reason="python3.8 is not supported yet by pytest-asyncio",
)
@pytest.mark.parametrize(
    "frame , text",
    [(getframe(), "ok"), (None, ""), (getframe(), 123)],
)
async def test_create_blank_frame_asyncio(frame, text):
    """
    Testing frame size reducer function
    """
    try:
        text_frame = create_blank_frame(frame=frame, text=text)
        logger.debug(text_frame.shape)
        assert not (text_frame is None)
    except Exception as e:
        if not (frame is None):
            pytest.fail(str(e))
