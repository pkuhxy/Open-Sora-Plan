# coding=utf-8
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import torch.nn as nn

from .vae import VideoAutoencoderKL

AE_MODEL_MAPPINGS = {"vae": VideoAutoencoderKL}


class AEModel(nn.Module):

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.ae = AE_MODEL_MAPPINGS[config.model_id](config)

    def get_model(self):
        return self.ae

    def encode(self, x):
        return self.model.encode(x)

    def decode(self, x):
        return self.model.decode(x)

    def forward(self, x):
        raise NotImplementedError("forward function is not implemented")


