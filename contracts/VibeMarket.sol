pragma solidity ^0.8.0;

contract VibeMarket {
    address public owner;
    uint256 public feePercentage = 1;

    event Purchase(address indexed buyer, address indexed seller, uint256 amount, uint256 fee, string itemId);

    constructor() {
        owner = msg.sender;
    }

    function buyItem(address payable seller, string memory itemId) external payable {
        require(msg.value > 0, "Price must be > 0");
        require(seller != address(0), "Invalid seller address");

        uint256 fee = (msg.value * feePercentage) / 100;
        uint256 sellerAmount = msg.value - fee;

        seller.transfer(sellerAmount);

        emit Purchase(msg.sender, seller, msg.value, fee, itemId);
    }

    function withdrawFees() external {
        require(msg.sender == owner, "Only owner");
        payable(owner).transfer(address(this).balance);
    }
}