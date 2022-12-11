# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from os import path

from nexusproto import DataTile_pb2 as nexusproto
from nexusproto.serialization import from_shaped_array

import sdap.processors


class TestDeleteTimeAxis(unittest.TestCase):
    def setUp(self):
        self.module = sdap.processors.DeleteUnitAxis("time")

    def test_delete_time_axis(self):
        test_file = path.join(path.dirname(__file__), 'dumped_nexustiles', 'avhrr_nonempty_nexustile.bin')

        with open(test_file, 'rb') as f:
            nexustile_str = f.read()

        nexus_tile_before = nexusproto.NexusTile.FromString(nexustile_str)

        sst_before = from_shaped_array(nexus_tile_before.tile.grid_tile.variable_data)

        self.assertEqual((1, 10, 10), sst_before.shape)

        results = list(self.module.process(nexustile_str))

        nexus_tile_after = results[0]

        sst_after = from_shaped_array(nexus_tile_after.tile.grid_tile.variable_data)

        self.assertEqual((10, 10), sst_after.shape)


if __name__ == '__main__':
    unittest.main()
