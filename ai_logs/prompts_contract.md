
# prompts_contract.md

Note: The following is a simulated contract prompt and design-log for demonstration. It is a human-curated example and NOT an actual LLM raw output. Label as "example/simulated" when presenting.

## Prompt (Example)

You are a blockchain contract engineer. Design a minimal and safe purchasing contract `VibeMarket` that enforces a 1% protocol fee, exposes a single purchase entrypoint, emits Purchase events, and allows the contract owner to withdraw accumulated fees. Provide interface definitions, key safety considerations, and a short rationale.

## Simulated Contract Thinking (Summary)

- Functional requirement: `buyItem(address payable seller, string itemId) payable` — compute 1% fee and forward the remainder to `seller`.
- Safety considerations: validate `msg.value > 0` and `seller != address(0)`; avoid reentrancy (use `transfer` or checks-effects-interactions pattern); consider limiting gas usage on forwards.
- Extensibility: include `withdrawFees()` for owner withdrawals; consider making `feePercentage` adjustable with strict access control if needed.

## Example Contract Snippet (implemented in `contracts/VibeMarket.sol`)

```solidity
pragma solidity ^0.8.0;

contract VibeMarket {
    address public owner;
    uint256 public feePercentage = 1;

    event Purchase(address indexed buyer, address indexed seller, uint256 amount, uint256 fee, string itemId);

    constructor() { owner = msg.sender; }

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
```

## Notes

- This is an illustrative record; production deployment and audits require professional review. Use this file to document design rationale in the repo.
