# config_module.py

import yaml

def create_default_config():
    default_config = {
        "seed": 1234,
        "trainer": {
            "gpus": 1,
            "overfit_batches": 0.0,
            "check_val_every_n_epoch": 1,
            "fast_dev_run": False,
            "max_epochs": 1,
            "min_epochs": 1,
            "num_sanity_val_steps": 0,
            "auto_lr_find": False,
            "checkpoint_callback": True
        },
        "callbacks": {
            "model_checkpoint": {
                "save_top_k": 1,
                "save_weights_only": True,
                "mode": "min",
                "monitor": "val/loss",
                "filename": "{epoch}-{val/loss:.2f}-{val/cer:.2f}"
            },
            "early_stopping": {
                "patience": 3,
                "mode": "min",
                "monitor": "val/loss",
                "min_delta": 0.001
            }
        },
        "data": {
            "batch_size": 32,
            "num_workers": 4,
            "pin_memory": False
        },
        "lit_model": {
            "lr": 0.001,
            "weight_decay": 0.0001,
            "milestones": [10],
            "gamma": 0.5,
            "d_model": 128,
            "dim_feedforward": 256,
            "nhead": 4,
            "dropout": 0.3,
            "num_decoder_layers": 3,
            "max_output_len": 150
        },
        "logger": {
            "project": "image-to-latex"
        }
    }

    with open("config.yaml", "w") as file:
        yaml.dump(default_config, file, default_flow_style=False)
