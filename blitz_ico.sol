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

    modifier can_purchase (uint _usd_value) {
        require(_usd_value * usd_to_blitz + total_coins_sold <= total_coins,
        "No more coins left to be sold");
        _;
    }

    modifier can_sell (address _investor, uint _blitz_value) {
        require(equity[_investor].blitz_equity >= _blitz_value,
        "Can't sell more Blitz coins than you own!");
        _;
    }

    // Equity in blitz
    function equity_in_blitz(address _investor) external view returns (uint blitz_equity) {
        blitz_equity = equity[_investor].blitz_equity;
    }

    // Equity in USD
    function equity_in_usd(address _investor) external view returns (uint usd_equity) {
        usd_equity = equity[_investor].usd_equity;
    }

    // buy Blitz
    function buy_blitz(address _investor, uint _usd_value) external can_purchase(_usd_value) {
        uint total = _usd_value * usd_to_blitz;
        equity[_investor].blitz_equity += total;
        equity[_investor].usd_equity += _usd_value;
        total_coins_sold += total;
    }

    // sell Blitz
    function sell_blitz(address _investor, uint _blitz_value) external can_sell(_investor, _blitz_value) {
        equity[_investor].blitz_equity -= _blitz_value;
        equity[_investor].usd_equity -= _blitz_value/1000;
        total_coins_sold -= _blitz_value;
    }

    // exchange Blitz
    function exchange_blitz(address _investor_selling, address _investor_buying, uint _blitz_value) external
    can_sell(_investor_selling, _blitz_value) {
        equity[_investor_selling].blitz_equity -= _blitz_value;
        equity[_investor_selling].usd_equity -= _blitz_value/usd_to_blitz;

        equity[_investor_buying].blitz_equity += _blitz_value;
        equity[_investor_buying].usd_equity += _blitz_value * usd_to_blitz;

    }
}
