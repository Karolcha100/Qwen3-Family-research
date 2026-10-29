from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast

import torch
from torch import nn
from transformers import PreTrainedModel


def at_least_float32(tensor: torch.Tensor) -> torch.Tensor:
    return tensor.to(torch.promote_types(tensor.dtype, torch.float32))


def decoder_layers(model: PreTrainedModel) -> nn.ModuleList:
    return model.model.layers


def down_projection(model: PreTrainedModel, layer_index: int) -> nn.Linear:
    return cast(nn.Linear, decoder_layers(model)[layer_index].get_submodule("mlp.down_proj"))


def intermediate_size(model: PreTrainedModel) -> int:
    return model.config.intermediate_size


@contextmanager
def layers_from(model: PreTrainedModel, first_layer_index: int) -> Iterator[None]:
    original_layers = decoder_layers(model)
    model.model.layers = nn.ModuleList(list(original_layers)[first_layer_index:])
    try:
        yield
    finally:
        model.model.layers = original_layers


@torch.no_grad()
def hidden_states_before_layer(model: PreTrainedModel, token_ids: torch.Tensor, layer_index: int) -> torch.Tensor:
    return model.model(input_ids=token_ids, output_hidden_states=True, use_cache=False).hidden_states[layer_index]


def final_hidden_states(model: PreTrainedModel, layer_input: torch.Tensor, first_layer_index: int) -> torch.Tensor:
    with layers_from(model, first_layer_index):
        return model.model(inputs_embeds=layer_input, use_cache=False).last_hidden_state
