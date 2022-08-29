# Copyright The PyTorch Lightning team.
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
from abc import ABC
from typing import List, Optional, Any, Dict

import torch
from torch.nn import Module
from torch.optim import Optimizer

from pytorch_lightning.plugins import LayerSync
from pytorch_lightning.plugins.environments.cluster_environment import ClusterEnvironment
from pytorch_lightning.plugins.io.checkpoint_plugin import CheckpointIO
from pytorch_lightning.plugins.precision import PrecisionPlugin
from pytorch_lightning.strategies.interface import PLStrategyInterface
from lightning_lite.lite.strategies.parallel import ParallelStrategy as CoreParallelStrategy
from lightning_lite.lite.accelerators.accelerator import Accelerator as CoreAccelerator
from pytorch_lightning.utilities.types import STEP_OUTPUT


class ParallelStrategy(CoreParallelStrategy, PLStrategyInterface, ABC):
    """Plugin for training with multiple processes in parallel."""

    def __init__(
        self,
        accelerator: Optional["CoreAccelerator"] = None,
        parallel_devices: Optional[List[torch.device]] = None,
        cluster_environment: Optional[ClusterEnvironment] = None,
        checkpoint_io: Optional[CheckpointIO] = None,
        precision_plugin: Optional[PrecisionPlugin] = None,
    ):
        super().__init__(accelerator=accelerator, checkpoint_io=checkpoint_io, precision_plugin=precision_plugin)
        self.parallel_devices = parallel_devices
        self.cluster_environment = cluster_environment
        self._layer_sync: Optional[LayerSync] = None

    @property
    def lightning_module(self) -> Optional["pl.LightningModule"]:
        """Returns the pure LightningModule without potential wrappers."""

    @property
    def model(self) -> Optional[Module]:
        """Returns the potentially wrapped LightningModule."""

    @model.setter
    def model(self, new_model: Optional[Module]) -> None:
        pass

    @property
    def optimizers(self) -> List[Optimizer]:
        pass

    @optimizers.setter
    def optimizers(self, optimizers: List[Optimizer]) -> None:
        pass

    @property
    def restore_checkpoint_after_setup(self) -> bool:
        """Override to delay restoring from checkpoint till after pre-dispatch. This is useful when the plugin
        requires all the setup hooks to run before loading checkpoint.

        Returns:
            If true, restore checkpoint after pre_dispatch.
        """

    @property
    def lightning_restore_optimizer(self) -> bool:
        """Override to disable Lightning restoring optimizers/schedulers.

        This is useful for plugins which manage restoring optimizers/schedulers.
        """

    @property
    def handles_gradient_accumulation(self) -> bool:
        """Whether the plugin handles gradient accumulation internally."""

    def connect(self, model: "pl.LightningModule") -> None:
        """Called by the accelerator to connect the accelerator and the model with this plugin."""

    def setup_optimizers(self, trainer: "pl.Trainer") -> None:
        """Creates optimizers and schedulers.

        Args:
            trainer: the Trainer, these optimizers should be connected to
        """

    def setup(self, trainer: "pl.Trainer") -> None:
        """Setup plugins for the trainer fit and creates optimizers.

        Args:
            trainer: the trainer instance
        """

    def training_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        """The actual training step.

        See :meth:`~pytorch_lightning.core.module.LightningModule.training_step` for more details
        """

    def post_training_step(self) -> None:
        pass

    def validation_step(self, *args: Any, **kwargs: Any) -> Optional[STEP_OUTPUT]:
        """The actual validation step.

        See :meth:`~pytorch_lightning.core.module.LightningModule.validation_step` for more details
        """

    def test_step(self, *args: Any, **kwargs: Any) -> Optional[STEP_OUTPUT]:
        """The actual test step.

        See :meth:`~pytorch_lightning.core.module.LightningModule.test_step` for more details
        """

    def predict_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        """The actual predict step.

        See :meth:`~pytorch_lightning.core.module.LightningModule.predict_step` for more details
        """

    def training_step_end(self, output: STEP_OUTPUT) -> STEP_OUTPUT:
        pass

    def validation_step_end(self, output: STEP_OUTPUT) -> STEP_OUTPUT:
        pass

    def test_step_end(self, output: STEP_OUTPUT) -> STEP_OUTPUT:
        pass

    def lightning_module_state_dict(self) -> Dict[str, Union[Any, Tensor]]:
        """Returns model state."""

    def on_train_start(self) -> None:
        """Called when train begins."""
        pass

    def on_validation_start(self) -> None:
        """Called when validation begins."""
        pass

    def on_test_start(self) -> None:
        """Called when test begins."""
        pass

    def on_predict_start(self) -> None:
        """Called when predict begins."""
        pass

    def on_train_end(self) -> None:
        """Called when train ends."""
        pass

    def on_validation_end(self) -> None:
        """Called when validation ends."""
        pass

    def on_test_end(self) -> None:
        """Called when test end."""
        pass

    def on_predict_end(self) -> None:
        """Called when predict ends."""
        pass

    def on_train_batch_start(self, batch: Any, batch_idx: int) -> None:
        """Called in the training loop before anything happens for that batch."""
        pass

    def dispatch(self, trainer: "pl.Trainer") -> None:
        """Hook to do something before the training/evaluation/prediction starts."""

    def reconciliate_processes(self, trace: str) -> None:
        """Function to re-conciliate processes on failure."""
