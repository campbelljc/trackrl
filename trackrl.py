import os
import copy
import pickle
import random
random.seed(1337)

from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.tf.visionnet import VisionNetwork
from ray.rllib.algorithms.ppo import PPOConfig

import gym
import pygame
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from openrct2.segments import *
from collisions import *
from track_io import *
from complex_net import ComplexInputNetworkMultipleShapes
from coaster_envs import *

ELMT_MAPPING = get_elmt_mapping()
# https://github.com/PathmindAI/nativerl/blob/f43e54486992e366c1b40c95d9da308ec9df7713/nativerl/python/pathmind_training/models.py
class TargetGrid3DActionMaskModel(TFModelV2):
    def __init__(self, obs_space, action_space, num_outputs, model_config, name, size, action_embed_size=len(ELMT_MAPPING)+1, *args, **kwargs):
        # filter sizes of 1x1,2x2,4x4 are bad
        # ref: https://medium.com/analytics-vidhya/how-to-choose-the-size-of-the-convolution-filter-or-kernel-size-for-cnn-86a55a1e2d15
        model_config["use_lstm"] = True
        model_config["conv_filters"] = {
            24: [
                #[32, [3, 3], 1],
                [64, [3, 3, 3], 2],#,1
                [64, [3, 3, 3], 2],
                [64, [3, 3, 3], 2],
                [64, [3, 3, 3], 2],
            ], (40, 16, 35): [
                [8, [5, 3, 5], 2],
                [16, [5, 3, 5], 2],
                [16, [5, 3, 5], 2],
                [16, [5, 2, 5], 2],
            ], (20, 20, 10): [
                [8, [3, 3, 3], 2],
                [16, [3, 3, 3], 2],
                [16, [3, 3, 3], 2],
                [16, [3, 3, 2], 2],
            ], (20, 20, 20): [
                [8, [3, 3, 3], 2],
                [16, [3, 3, 3], 2],
                [16, [3, 3, 3], 2],
                [16, [3, 3, 3], 2],
            ], (20, 20, 30): [
                [8, [3, 3, 5], 2],
                [16, [3, 3, 5], 2],
                [16, [3, 3, 5], 2],
                [16, [3, 3, 4], 2],
            ]
        }
        assert size in model_config["conv_filters"]
        super().__init__(obs_space, action_space, num_outputs, model_config, name, *args, **kwargs)        
        self.action_embed_model = ComplexInputNetworkMultipleShapes(Dict({
                "grid_obs": Box(low=0, high=16, shape=(*size, 8), dtype=np.byte),
                "targets": Box(low=-1, high=1, shape=(len(TARGET_RANGES),)),
                "values": Box(low=-1, high=1, shape=(len(TARGET_RANGES),)),

                #**{f'target_{target}': Box(low=-1, high=1, shape=(1,)) for target in TARGET_RANGES},
                #**{f'cur_{target}': Box(low=-1, high=1, shape=(1,)) for target in TARGET_RANGES},
            }), action_space, action_embed_size, model_config, name + "_action_embedding"
        )
    
    def forward(self, input_dict, state, seq_lens):
        action_mask = input_dict["obs"]["action_mask"]
        obs = input_dict["obs"]["observations"]
        
        squares = []
        for x in ["grid", "chain_lift", "vangle_start", "vangle_end", "bank_start", "bank_end", "special_flags", "brakes"]:
            squares.append(obs[x])
            del obs[x]
        
        new_obs = {
            'grid_obs': np.stack(squares, axis=-1),
            **obs
        }
        
        action_embedding, _ = self.action_embed_model({"obs": new_obs})
        inf_mask = tf.maximum(tf.math.log(action_mask), tf.float32.min)
        return action_embedding + inf_mask, state
 
    def value_function(self):
        return self.action_embed_model.value_function()

from ray.rllib.algorithms.callbacks import DefaultCallbacks
class MyCallback(DefaultCallbacks):
    def on_episode_end(self, *, worker, base_env, policies, episode, env_index, **kwargs):
        episode.custom_metrics["coaster_value"] = episode.last_raw_obs_for()['value']
        episode.custom_metrics["excitement"] = episode.last_raw_obs_for()['excitement']
        episode.custom_metrics["intensity"] = episode.last_raw_obs_for()['intensity']
        episode.custom_metrics["nausea"] = episode.last_raw_obs_for()['nausea']
        episode.custom_metrics["reached_station"] = episode.last_raw_obs_for()['reached_station']
        episode.custom_metrics["backtracks"] = episode.last_raw_obs_for()['backtracks']
        
        for target in TARGET_RANGES:
            episode.custom_metrics[target] = episode.last_raw_obs_for()[target]

env, model = TargetGridCoasterEnv, TargetGrid3DActionMaskModel

NUM_ROLLOUT_WORKERS = 8
if NUM_ROLLOUT_WORKERS < 8:
    input("Warning: Rollout workers less than 8.")
env_config = {
    "size": (40, 16, 35), #(20, 20, 30),
    #"elmt_mapping": ELMT_MAPPING
    #"render": True,
    "max_track_coords": 232, #145, #232
    "limit_intensity": True
}
from ray import air, tune
config = (
    PPOConfig()
    .environment(env, env_config=env_config)
    .rollouts(num_rollout_workers=NUM_ROLLOUT_WORKERS)
    .callbacks(MyCallback)
    #.resources(num_gpus=1)
    .framework("tf2")
    .training(model={
        "custom_model": model,
        "custom_model_config": {
            "size": env_config["size"],
        }},
        #vf_clip_param=1000,
        #entropy_coeff=0.1,
        #"fcnet_hiddens": [64, 64]
    )
    #.training() #lr=5e-05)
    .evaluation(evaluation_num_workers=1)
)

if __name__ == '__main__':
    #input("building")
    
    #algo = config.build()  # 2. build the algorithm,
    #for _ in range(5):
    #    print(algo.train())  # 3. train it,
    #algo.evaluate()  # 4. and evaluate it.

    #'''
    stop = {
        "training_iteration": 30000,
        "timesteps_total": 600000,
        "episode_reward_mean": 30000,
    }

    from ray.tune.logger import pretty_print
    
    tuner = tune.Tuner(
        "PPO",
        param_space=config.to_dict(),
        run_config=air.RunConfig(stop=stop, verbose=2,
            checkpoint_config=air.CheckpointConfig(
                checkpoint_frequency=1, checkpoint_at_end=True
            ),
        ),
    )
    results = tuner.fit()
    #'''
    
    from ray.rllib.algorithms.algorithm import Algorithm
    
    print("Training completed. Restoring new Trainer for action inference.")
    # Get the last checkpoint from the above training run.
    checkpoint = results.get_best_result().checkpoint
    # Create new Algorithm and restore its state from the last checkpoint.
    algo = Algorithm.from_checkpoint(checkpoint)
    
    # Create the env to do inference in.
    env = env(env_config)
    obs = env.reset()

    num_episodes = 0
    episode_reward = 0.0

    while num_episodes < 1 :
        # Compute an action (`a`).
        a = algo.compute_single_action(
            observation=obs,
            explore=True,
            policy_id="default_policy",  # <- default value
        )
        # Send the computed action `a` to the env.
        obs, reward, done, info = env.step(a, verbose=True)
        episode_reward += reward
        # Is the episode `done`? -> Reset.
        if done:
            if episode_reward > 0:
                env.save_track(f"{checkpoint._uuid}-{num_episodes}")
                num_episodes += 1
            print(f"Episode done: Total reward = {episode_reward}; excitement: {env.col_datas[-1]._vars['excitement']}, intensity: {env.col_datas[-1]._vars['intensity']}, nausea: {env.col_datas[-1]._vars['nausea']}, value: {env.col_datas[-1]._vars['value']}; num: {env.num}")
            obs = env.reset()
            episode_reward = 0.0

    algo.stop()