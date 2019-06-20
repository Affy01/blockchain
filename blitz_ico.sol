pragma solidity >=0.4.22 <0.6.0;

contract Blitz {

    struct Equity{
        uint usd_equity;
        uint blitz_equity;
    }

    // Total Blitz coins. 1M coins
    uint private total_coins = 1000000;

    // Total coins sold
    uint private total_coins_sold = 0;

    // USD to Blitz conversion
    uint public usd_to_blitz = 1000;

    mapping(address => Equity) equity;

    modifier can_purchase (uint usd_value) {
        require(usd_value * usd_to_blitz + total_coins_sold <= total_coins,
        "No more coins left to be sold");
        _;
    }

    modifier can_sell (address investor, uint blitz_value) {
        require(equity[investor].blitz_equity >= blitz_value,
        "Can't sell more Blitz coins than you own!");
        _;
    }

    // Equity in blitz
    function equity_in_blitz(address investor) external view returns (uint blitz_equity) {
        blitz_equity = equity[investor].blitz_equity;
    }

    // Equity in USD
    function equity_in_usd(address investor) external view returns (uint usd_equity) {
        usd_equity = equity[investor].usd_equity;
    }

    // buy Blitz
    function buy_blitz(address investor, uint usd_value) external can_purchase(usd_value) {
        uint total = usd_value * usd_to_blitz;
        equity[investor].blitz_equity += total;
        equity[investor].usd_equity += usd_value;
        total_coins_sold += total;
    }

    // sell Blitz
    function sell_blitz(address investor, uint blitz_value) external can_sell(investor, blitz_value) {
        equity[investor].blitz_equity -= blitz_value;
        equity[investor].usd_equity -= blitz_value/1000;
        total_coins_sold -= blitz_value;
    }

    // exchange Blitz
    function exchange_blitz(address investor_selling, address investor_buying, uint blitz_value) external
    can_sell(investor_selling, blitz_value) {
        equity[investor_selling].blitz_equity -= blitz_value;
        equity[investor_selling].usd_equity -= blitz_value/usd_to_blitz;

        equity[investor_buying].blitz_equity += blitz_value;
        equity[investor_buying].usd_equity += blitz_value * usd_to_blitz;

    }
}
