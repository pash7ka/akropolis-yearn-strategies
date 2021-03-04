 
// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "../vakro/AdelVAkroSwap.sol";
import "../../interfaces/IERC20Mintable.sol";
import "../../interfaces/delphi/IStakingPool.sol";

contract TestAdelVAkroSwap is AdelVAkroSwap {
    function initialize(address _akro, address _adel, address _vakro) public override initializer {
        AdelVAkroSwap.initialize(_akro, _adel, _vakro);
    }    

    /**
     * @notice Verifies merkle proofs of user to be elligible for swap
     * @param _account Address of a user
     * @param _merkleRootIndex Index of a merkle root to be used for calculations
     * @param _adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param _merkleProofs Array of consiquent merkle hashes
     */
    function verifyMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) public override view returns(bool)
    {
        return true;
    }
}