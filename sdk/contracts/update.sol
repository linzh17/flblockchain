pragma solidity ^0.4.24;

import "./ParallelContract.sol";  // 引入ParallelContract.sol
contract update is ParallelContract{
    /**
    *nodeid update 的次数
    *cur_round 当前训练轮次
    * up_weight 本地更新的模型权重
    * up_weight_sum 当前训练轮次更新权重之和
     */
    uint256 nodeid;
    uint256 cur_round;
    bytes up_weight;
    bytes up_weight_sum;
    constructor() public{
        nodeid = 0;
        cur_round = 1;
    }
    function get()  public returns(bytes sum){
        // try catch
        return up_weight_sum;
    }
     function get_round()  public returns(uint256 round){
        // try catch
        return cur_round;
    }
    
  function set(bytes weight,bytes sum) public {
        up_weight = weight;
        up_weight_sum = sum;
        nodeid = nodeid + 1;
        /*
        * 判断轮次（假设每五次update 更新轮次）
        *返回当前轮次
        *client 对返回轮次进行检查 如果返回轮次与client 轮次不同
        *则该client 拉取up_weight_sum,在client进行平均计算 并调用gmodel 合约进行更新
        * 调用clean()对update 中的up_weight_sum 进行初始化
        */
        if (nodeid % 2 == 0){
            cur_round = cur_round+1;
        }
    }


    function clean(bytes sum)public{
        up_weight_sum = sum;
    }


     // 注册可以并行的合约接口
    function enableParallel() public{
        // 函数定义字符串（注意","后不能有空格）,参数的前几个是互斥参数（设计函数时互斥参数必须放在前面
        registerParallelFunction("set(bytes,bytes)", 2); // critical: string string
        registerParallelFunction("get(bytes)", 1); // critical: string string
        registerParallelFunction("get_round(uint256)", 1); // critical: string string
    } 
    // 注销并行合约接口
    function disableParallel() public{
        unregisterParallelFunction("set(bytes,bytes)");
        unregisterParallelFunction("get(bytes)");
        unregisterParallelFunction("get_round(uint256)");
    } 
}



