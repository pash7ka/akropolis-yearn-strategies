import pytest
import brownie
from web3 import Web3
from hexbytes import HexBytes

ADEL_AKRO_RATE = 15

def get_users():
    users = (
        '0xc97ad401c75e6bfb5694899cd3271485d27c6ea4', # User to swap from wallet
        '0xf47f63cbb47b75967b29f4749959507db43b1038', # User to swap from stake
        '0xb1f9a358003ae5145805e936db3af3c22368e324', # User to swap from rewards (Adel staking)
        '0xa215f1b06e7945d331f2df30961027123947a40d', # User to swap from both stake and rewards (Adel staking)
        '0x8efd9addd8de6a4e64664d1893dec51f8c3339e9', # User to swap from wallet and stake to get change to the wallet
        '0xeb1a799769fc69e84440f9d162d12b196e6e369c'  # User to swap from rewards (Adel and Akro stakings)
    )
    return users

def users_proofs():
    users = get_users()
    proofs = [
        {   'amount_wallet': 1036421477600000000000,
            'amount_stake': 0,
            'amount_rewards': 0,
            'rootIndex': 0,
            'maxAmount': 1036421477600000000000,
            'proofs': [
                HexBytes("0xf998860e2d92d57193e8083b5a10ea2a58e3de4a8a6166c936b868982c5ec6c5"),
                HexBytes("0x95cddcd8fe4312ff02e412d4f1a0be2716053014d26bd70e11d363e79a2ba958"),
                HexBytes("0x079d7ae5d25d5dfa25259faf9fe3941ceb2b0a893490825226b79dfa920f3c4e"),
                HexBytes("0x875d4362ebaccfa1b902cdb5d83ba1955208a232823204a46aa40733bc579633"),
                HexBytes("0x59670fe60a33184d3f6224b8911f9af72805185d718b1c936fca8ae17705c5b8"),
                HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
                HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
            ]},
        {'amount_rewards_from_adel': 10568296513606745240,
         'amount_rewards_from_akro': 17638283950673047945,
         'amount_wallet': 530317137800000000000,
         'amount_stake': 7906230352639412586431,
         'amount_rewards': 10568296513606745240 + 17638283950673047945,
         'rootIndex': 0,
         'maxAmount': 8464754070903692379616,
         'proofs': [
            HexBytes("0x8139e229faedffab87a43478e67b81e63df0fcaee7976cecf757924da39cfb6b"),
            HexBytes("0xab66dbc0d1555593e61fe8ff6538387f646bdcb367f4fb179f3e6b2982fa07b3"),
            HexBytes("0xa26d66865bffb0870f11c9c5331a474360099d174390825128cf34479909c950"),
            HexBytes("0x7eae330d27403dc446669c513cdec5ebe7750ccfcb3031a2a93bce63bf31fd8c"),
            HexBytes("0x59670fe60a33184d3f6224b8911f9af72805185d718b1c936fca8ae17705c5b8"),
            HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
            HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
        ]},
        {   'amount_wallet': 31481786698989648049,
            'amount_stake': 302885125819850880724,
            'amount_rewards': 3670344697071449027,
            'rootIndex': 0,
            'maxAmount': 338037257215911977800,
            'proofs': [
                HexBytes("0x2f38bdff1807dfb912295e05d915e5e30234eb9282c635edc44ae1f6cab38327"),
                HexBytes("0xdae130919ffbe63bdc6ac438053987ed4877b9a304dc9bb94770dd6437b12bb8"),
                HexBytes("0x314f80fa2fbffda0d3adae944c1fbd7d5fc5087327b5444015e28d1abf25f0ba"),
                HexBytes("0x1a2e5a7d0ecb0d02601777d80643bfefe3ab0ef4087dbe82b0155befd19f4156"),
                HexBytes("0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"),
                HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
                HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
            ]},
        {'amount_wallet': 4130000000000000000,
         'amount_stake': 122202583170062799350,
         'amount_rewards': 8454965720780178145,
         'rootIndex': 0,
         'maxAmount': 134787548890842977495,
         'proofs': [
            HexBytes("0xb6967a2e899018c421adc71a0433590b09051a5ec02c10c6c9a268f7dcf1103c"),
            HexBytes("0x587c24103fff0fa07849a8917193ed6b02a6a3d9e534531f90b73a0fdacac26e"),
            HexBytes("0xe8243531c2b48bede9404bc63b735f79a494f392d6f8d75627a5995ac6fa640b"),
            HexBytes("0x3c422af1c5ab9de36ce5eb4c8c0e0eeca9162cc2f6804754bbb336d57cf65dce"),
            HexBytes("0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"),
            HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
            HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
        ]},
        {   'amount_wallet': 683108047500000000000,
            'amount_stake': 20424450350752168953589,
            'amount_rewards': 0,
            'rootIndex': 0,
            'maxAmount': 21107558398252168953589,
            'proofs': [
                HexBytes("0x446193ccfd7dc68e9f394f5e503f07c55647ad08306150cf9d5980954dd4fd69"),
                HexBytes("0xbe25a70184c7817af7ddac562b6e2cd698ff4cf9e98fee99ca1fad046ca0496f"),
                HexBytes("0x314f80fa2fbffda0d3adae944c1fbd7d5fc5087327b5444015e28d1abf25f0ba"),
                HexBytes("0x1a2e5a7d0ecb0d02601777d80643bfefe3ab0ef4087dbe82b0155befd19f4156"),
                HexBytes("0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"),
                HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
                HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
            ]},
        {'amount_rewards_from_adel': 69313632956836605332,
         'amount_rewards_from_akro': 58070532741279831725,
         'amount_wallet': 24940000000000000000,
         'amount_stake': 1001814232718785944543,
         'amount_rewards': 69313632956836605332 + 58070532741279831725,
         'rootIndex': 0,
         'maxAmount': 1154138398416902381600,
         'proofs': [
            HexBytes("0x4bf7dc3a11a7d09196e12a905c785b5dd1aff4d11901339da2dfdb2bfca41c4d"),
            HexBytes("0xd359c34d6f6a0fafeeb0c7a681e6155236461f207cd6c13e6ac31de7e0e77d71"),
            HexBytes("0x079d7ae5d25d5dfa25259faf9fe3941ceb2b0a893490825226b79dfa920f3c4e"),
            HexBytes("0x875d4362ebaccfa1b902cdb5d83ba1955208a232823204a46aa40733bc579633"),
            HexBytes("0x59670fe60a33184d3f6224b8911f9af72805185d718b1c936fca8ae17705c5b8"),
            HexBytes("0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"),
            HexBytes("0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849")
        ]}
    ]

    return dict(zip(users, proofs))

def merkle_roots():
    return [HexBytes('0x15a33c8b140d00e2b0147768296e9d275a2f7ef388e41c292f7eb5e658d5ebef')]

total_adel_swapped = 0
total_stake_withdrawn = 0
total_rewards_from_adel = 0
total_rewards_from_akro = 0
staking_adel_before = 0
rewards_on_adel_before = 0
rewards_on_akro_before = 0

total_adel_change = 0

def test_initial_balances(chain, owner, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool, prepare_swap, prepare_stakings):
    global staking_adel_before
    staking_adel_before = adelstakingpool.totalStaked()
    global rewards_on_adel_before
    rewards_on_adel_before = adel.balanceOf(adelstakingpool.address) - adelstakingpool.totalStaked()
    global rewards_on_akro_before
    rewards_on_akro_before = adel.balanceOf(akrostakingpool.address)

    # Prepare vAkro and swap
    vakroSwap.setMerkleRoots(merkle_roots(), {'from': owner})
    vakro.setVestingCliff(0, {'from': owner})
    start = chain.time() + 1000
    vakro.setVestingStart(start, {'from': owner})
    chain.mine(1)

    assert adel.balanceOf(vakro.address) == 0
    assert adel.balanceOf(vakroSwap.address) == 0
    assert adel.balanceOf(adelstakingpool.address) != 0


def test_swap_adel_1(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()

    ###
    #  Can swap from the wallet
    ###
    user_adel_balance_before = adel.balanceOf(user_for_wallet)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_wallet)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_wallet, adel.address) + akrostakingpool.rewardBalanceOf(user_for_wallet, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_wallet) == 0
    assert vakro.balanceOf(user_for_wallet) == 0

    adel.approve(vakroSwap.address, proofs_dict[user_for_wallet]['amount_wallet'], {'from': user_for_wallet})
    vakroSwap.swapFromAdel(
        proofs_dict[user_for_wallet]['amount_wallet'],
        proofs_dict[user_for_wallet]['rootIndex'],
        proofs_dict[user_for_wallet]['maxAmount'],
        proofs_dict[user_for_wallet]['proofs'],
            {'from': user_for_wallet})
    
    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_wallet]['amount_wallet']

    user_adel_balance_after = adel.balanceOf(user_for_wallet)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_wallet)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_wallet, adel.address) + akrostakingpool.rewardBalanceOf(user_for_wallet, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before - user_adel_balance_after == proofs_dict[user_for_wallet]['amount_wallet']
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_wallet]['amount_wallet']

    assert total_staked_before == total_staked_after
    assert user_adel_staked_before == user_adel_staked_after
    assert user_adel_rewards_before == user_adel_rewards_after

    assert vakro.balanceOf(user_for_wallet) == ADEL_AKRO_RATE * proofs_dict[user_for_wallet]['amount_wallet']
    assert vakroSwap.adelSwapped(user_for_wallet) == proofs_dict[user_for_wallet]['amount_wallet']

def test_swap_adel_2(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()

    ###
    # Can swap from the stake
    ###
    user_adel_balance_before = adel.balanceOf(user_for_stake)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_stake)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_stake, adel.address) + akrostakingpool.rewardBalanceOf(user_for_stake, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_stake) == 0
    assert vakro.balanceOf(user_for_stake) == 0

    with brownie.reverts():
        vakroSwap.swapFromStakedAdel(
            proofs_dict[user_for_stake]['rootIndex'],
            proofs_dict[user_for_stake]['maxAmount'],
            proofs_dict[user_for_stake]['proofs'],
                {'from': user_for_stake})

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_stake]['rootIndex'],
        proofs_dict[user_for_stake]['maxAmount'],
        proofs_dict[user_for_stake]['proofs'],
            {'from': user_for_stake})

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_stake]['rootIndex'],
        proofs_dict[user_for_stake]['maxAmount'],
        proofs_dict[user_for_stake]['proofs'],
            {'from': user_for_stake})

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_stake]['amount_stake'] + proofs_dict[user_for_stake]['amount_rewards']
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_stake]['amount_stake']
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_stake]['amount_rewards_from_adel']
    global total_rewards_from_akro
    total_rewards_from_akro += proofs_dict[user_for_stake]['amount_rewards_from_akro']

    user_adel_balance_after = adel.balanceOf(user_for_stake)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_stake)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_stake, adel.address) + akrostakingpool.rewardBalanceOf(user_for_stake, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_stake]['amount_stake'] + proofs_dict[user_for_stake]['amount_rewards']

    assert total_staked_before - total_staked_after == proofs_dict[user_for_stake]['amount_stake']
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_stake) == ADEL_AKRO_RATE * (proofs_dict[user_for_stake]['amount_stake'] + proofs_dict[user_for_stake]['amount_rewards'])
    assert vakroSwap.adelSwapped(user_for_stake) == proofs_dict[user_for_stake]['amount_stake'] + proofs_dict[user_for_stake]['amount_rewards']

def test_swap_adel_3(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()

    ###
    # Can swap from rewards
    ###
    user_adel_balance_before = adel.balanceOf(user_for_rewards)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_rewards)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_rewards, adel.address) + akrostakingpool.rewardBalanceOf(user_for_rewards, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_rewards) == 0
    assert vakro.balanceOf(user_for_rewards) == 0

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_rewards]['rootIndex'],
        proofs_dict[user_for_rewards]['maxAmount'],
        proofs_dict[user_for_rewards]['proofs'],
            {'from': user_for_rewards})

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_rewards]['amount_rewards']
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_rewards]['amount_rewards']

    user_adel_balance_after = adel.balanceOf(user_for_rewards)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_rewards)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_rewards, adel.address) + akrostakingpool.rewardBalanceOf(user_for_rewards, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_rewards]['amount_rewards']

    assert total_staked_before == total_staked_after
    assert user_adel_staked_before == user_adel_staked_after
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_rewards) == ADEL_AKRO_RATE * proofs_dict[user_for_rewards]['amount_rewards']
    assert vakroSwap.adelSwapped(user_for_rewards) == proofs_dict[user_for_rewards]['amount_rewards']

def test_swap_adel_4(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()

    ###
    # Can swap from stake and rewards
    ###
    user_adel_balance_before = adel.balanceOf(user_for_stake_reward)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_stake_reward)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_stake_reward, adel.address) + akrostakingpool.rewardBalanceOf(user_for_stake_reward, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_stake_reward) == 0
    assert vakro.balanceOf(user_for_stake_reward) == 0


    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_stake_reward]['rootIndex'],
        proofs_dict[user_for_stake_reward]['maxAmount'],
        proofs_dict[user_for_stake_reward]['proofs'],
            {'from': user_for_stake_reward})

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_stake_reward]['rootIndex'],
        proofs_dict[user_for_stake_reward]['maxAmount'],
        proofs_dict[user_for_stake_reward]['proofs'],
            {'from': user_for_stake_reward})

    global total_adel_swapped
    total_adel_swapped += (proofs_dict[user_for_stake_reward]['amount_stake'] + proofs_dict[user_for_stake_reward]['amount_rewards'])
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_stake_reward]['amount_stake']
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_stake_reward]['amount_rewards']

    user_adel_balance_after = adel.balanceOf(user_for_stake_reward)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_stake_reward)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_stake_reward, adel.address) + akrostakingpool.rewardBalanceOf(user_for_stake_reward, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_stake_reward]['amount_stake'] + proofs_dict[user_for_stake_reward]['amount_rewards']

    assert total_staked_before - total_staked_after == proofs_dict[user_for_stake_reward]['amount_stake']
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_stake_reward) == ADEL_AKRO_RATE * (proofs_dict[user_for_stake_reward]['amount_stake'] + proofs_dict[user_for_stake_reward]['amount_rewards'])
    assert vakroSwap.adelSwapped(user_for_stake_reward) == proofs_dict[user_for_stake_reward]['amount_stake'] + proofs_dict[user_for_stake_reward]['amount_rewards']

def test_swap_adel_5(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()

    ###
    # Change is sent to the wallet
    ###
    user_adel_balance_before = adel.balanceOf(user_for_change)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_change)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_change, adel.address) + akrostakingpool.rewardBalanceOf(user_for_change, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_change) == 0
    assert vakro.balanceOf(user_for_change) == 0

    over_adel = proofs_dict[user_for_stake]['amount_wallet']
    assert over_adel > 0 and over_adel < proofs_dict[user_for_change]['amount_stake']
    adel.transfer(user_for_change, over_adel, {'from': user_for_stake})
    amount_to_swap = proofs_dict[user_for_change]['amount_wallet'] + over_adel
    adel.approve(vakroSwap.address, amount_to_swap, {'from': user_for_change})
    vakroSwap.swapFromAdel(
        amount_to_swap,
        proofs_dict[user_for_change]['rootIndex'],
        proofs_dict[user_for_change]['maxAmount'],
        proofs_dict[user_for_change]['proofs'],
            {'from': user_for_change})

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_change]['rootIndex'],
        proofs_dict[user_for_change]['maxAmount'],
        proofs_dict[user_for_change]['proofs'],
            {'from': user_for_change})

    global total_adel_swapped
    total_adel_swapped += (amount_to_swap + proofs_dict[user_for_change]['amount_stake'])
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_change]['amount_stake']

    user_adel_balance_after = adel.balanceOf(user_for_change)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_change)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_change, adel.address) + akrostakingpool.rewardBalanceOf(user_for_change, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    global total_adel_change
    total_adel_change = (amount_to_swap +
                         proofs_dict[user_for_change]['amount_stake'] -
                         proofs_dict[user_for_change]['maxAmount'])

    assert user_adel_balance_before - user_adel_balance_after == proofs_dict[user_for_change]['amount_wallet'] - total_adel_change
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_change]['maxAmount']

    assert total_staked_before - total_staked_after == proofs_dict[user_for_change]['amount_stake']
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_change) == ADEL_AKRO_RATE * proofs_dict[user_for_change]['maxAmount']
    assert vakroSwap.adelSwapped(user_for_change) == proofs_dict[user_for_change]['maxAmount']

def test_swap_adel_6(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    user_for_wallet, user_for_stake, user_for_rewards, user_for_stake_reward, user_for_change, user_for_both_rewards = get_users()
    ###
    # Rewards from both stakings
    ###
    user_adel_balance_before = adel.balanceOf(user_for_both_rewards)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(user_for_both_rewards)
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(user_for_both_rewards, adel.address) + akrostakingpool.rewardBalanceOf(user_for_both_rewards, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_both_rewards) == 0
    assert vakro.balanceOf(user_for_both_rewards) == 0

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_both_rewards]['rootIndex'],
        proofs_dict[user_for_both_rewards]['maxAmount'],
        proofs_dict[user_for_both_rewards]['proofs'],
            {'from': user_for_both_rewards})

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_both_rewards]['amount_rewards']
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_both_rewards]['amount_rewards_from_adel']
    global total_rewards_from_akro
    total_rewards_from_akro += proofs_dict[user_for_both_rewards]['amount_rewards_from_akro']

    user_adel_balance_after = adel.balanceOf(user_for_both_rewards)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_both_rewards)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(user_for_both_rewards, adel.address) + akrostakingpool.rewardBalanceOf(user_for_both_rewards, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert swap_adel_balance_after - swap_adel_balance_before == proofs_dict[user_for_both_rewards]['amount_rewards']

    assert total_staked_before == total_staked_after
    assert user_adel_staked_after == user_adel_staked_before
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_both_rewards) == ADEL_AKRO_RATE * proofs_dict[user_for_both_rewards]['amount_rewards']
    assert vakroSwap.adelSwapped(user_for_both_rewards) == proofs_dict[user_for_both_rewards]['amount_rewards']
    
    
def test_final_balances(adel, akro, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    ###
    # All calculations match
    ###
    staking_adel_after = adelstakingpool.totalStaked()
    rewards_on_adel_after = adel.balanceOf(adelstakingpool.address) - adelstakingpool.totalStaked()
    rewards_on_akro_after = adel.balanceOf(akrostakingpool.address)

    global total_adel_swapped
    global total_adel_change
    global total_stake_withdrawn
    global total_rewards_from_adel
    global total_rewards_from_akro
    global staking_adel_before
    global rewards_on_adel_before
    global rewards_on_akro_before

    assert adel.balanceOf(vakroSwap.address) == total_adel_swapped - total_adel_change
    assert staking_adel_before - staking_adel_after == total_stake_withdrawn
    assert rewards_on_adel_before - rewards_on_adel_after == total_rewards_from_adel
    assert rewards_on_akro_before - rewards_on_akro_after == total_rewards_from_akro
    assert akro.balanceOf(vakroSwap.address) == 0
    assert vakro.balanceOf(vakroSwap.address) == 0
