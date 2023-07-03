pragma solidity ^0.8.12;

contract Crowdfunding{

struct transaction{
             uint reqid;
	     uint policyid;
	     uint userid;
	     uint amount;
             string date;
  }
transaction [] alltrans;
uint total=0;

function addTransaction(uint reqida,uint policyida,uint userida, uint amounta,string memory datea) public{
	transaction memory e = transaction(reqida,policyida,userida,amounta,datea);
	alltrans.push(e);
 
  }
function viewTransaction(uint reqid) public view returns(uint,uint,uint,string memory){
	uint i;
	    for(i=0;i<alltrans.length;i++){
			transaction memory e = alltrans[i];
			if(e.reqid==reqid)
				{
					return(e.policyid,e.userid,e.amount,e.date);
				}

 
                }
		return(0,0,0,"0");
  }
}
