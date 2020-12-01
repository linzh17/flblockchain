pragma solidity ^0.4.24;

contract gmodel{

    uint256 cur_round;
    bytes model_weight;

    
    event modelupdate (uint256 cur_round,bytes model_weight);

    constructor() public{
        cur_round = 0;
    }
    function get_weight() public returns(bytes weight){
        return model_weight;
    }
    function get_round() public returns(uint256 round){
        return cur_round;
    }
  function set(bytes weight) public{
        model_weight = weight;
        cur_round = cur_round + 1;
        //触发更新事件，client 监听到事件后 更新本地模型 以及训练轮次
        emit modelupdate(cur_round,model_weight);
            
        }
}


