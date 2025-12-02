// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VibeMarket {
    address public owner;
    uint256 public feePercentage = 1; // 1% Fee

    // 事件：购买成功后触发，方便前端监听（虽然我们本次只用 tx hash）
    event Purchase(address indexed buyer, address indexed seller, uint256 amount, uint256 fee, string itemId);

    constructor() {
        owner = msg.sender;
    }

    // 核心函数：买东西
    // seller: 卖家的钱包地址
    // itemId: 商品ID (字符串)
    function buyItem(address payable seller, string memory itemId) external payable {
        require(msg.value > 0, "Price must be > 0");
        require(seller != address(0), "Invalid seller address");

        // 计算 1% 手续费
        uint256 fee = (msg.value * feePercentage) / 100;
        uint256 sellerAmount = msg.value - fee;

        // 99% 给卖家
        seller.transfer(sellerAmount);
        
        // 1% 留在合约里（也就是给平台/你）
        // 也可以直接 payable(owner).transfer(fee); 但存在合约里更像 Protocol

        emit Purchase(msg.sender, seller, msg.value, fee, itemId);
    }

    // 只有你能提款
    function withdrawFees() external {
        require(msg.sender == owner, "Only owner");
        payable(owner).transfer(address(this).balance);
    }
}