import json
import time
import hashlib
import re

class SelfHealingContract:
    """Smart contract that can self-heal"""
    
    def __init__(self, contract_code):
        self.contract_code = contract_code
        self.version = "1.0"
        self.creation_time = time.time()
        self.healing_count = 0
        self.vulnerabilities_fixed = 0
        self.state = {}
        self.security_scanner = SecurityScanner()
        
    def execute(self, function_name, *args):
        """Execute contract function"""
        print(f"\n⚡ Executing function: {function_name}")
        
        vulnerabilities = self.security_scanner.scan(self.contract_code)
        
        if vulnerabilities:
            print(f"🔍 Vulnerabilities found: {len(vulnerabilities)}")
            healed_code = self._auto_heal(vulnerabilities)
            
            if healed_code != self.contract_code:
                self.healing_count += 1
                self.vulnerabilities_fixed += len(vulnerabilities)
                self.contract_code = healed_code
                print(f"✅ Contract auto-healed! Version: {self.version}")
        
        if function_name == "transfer":
            return self._transfer(*args)
        elif function_name == "balance":
            return self._get_balance(*args)
        elif function_name == "mint":
            return self._mint(*args)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def _transfer(self, from_addr, to_addr, amount):
        """Transfer funds"""
        if amount <= 0:
            return {"error": "Amount must be positive"}
        
        if from_addr not in self.state:
            self.state[from_addr] = 0
        
        if to_addr not in self.state:
            self.state[to_addr] = 0
        
        if self.state[from_addr] < amount:
            return {"error": "Insufficient funds"}
        
        self.state[from_addr] -= amount
        self.state[to_addr] += amount
        
        return {
            "success": True,
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "new_balance_from": self.state[from_addr],
            "new_balance_to": self.state[to_addr]
        }
    
    def _get_balance(self, address):
        """Get balance"""
        return {
            "address": address,
            "balance": self.state.get(address, 0)
        }
    
    def _mint(self, address, amount):
        """Create new tokens"""
        if amount <= 0:
            return {"error": "Amount must be positive"}
        
        if address not in self.state:
            self.state[address] = 0
        
        self.state[address] += amount
        
        return {
            "success": True,
            "address": address,
            "minted": amount,
            "new_balance": self.state[address]
        }
    
    def _auto_heal(self, vulnerabilities):
        """Auto-heal vulnerabilities"""
        healed_code = self.contract_code
        
        for vuln in vulnerabilities:
            if vuln['type'] == 'reentrancy':
                healed_code = self._fix_reentrancy(healed_code)
            elif vuln['type'] == 'overflow':
                healed_code = self._fix_overflow(healed_code)
            elif vuln['type'] == 'access_control':
                healed_code = self._fix_access_control(healed_code)
        
        return healed_code
    
    def _fix_reentrancy(self, code):
        if "transfer" in code and "call.value" in code:
            code = code.replace("call.value", "transfer")
            code += "\n// AUTO-FIXED: Reentrancy vulnerability patched"
        
        return code
    
    def _fix_overflow(self, code):
        patterns = [r"(\w+)\s*\+\s*(\w+)", r"(\w+)\s*\-\s*(\w+)"]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                check = f"require({match[0]} + {match[1]} >= {match[0]}, 'Overflow')"
                if check not in code:
                    code += f"\n{check}"
        
        return code
    
    def _fix_access_control(self, code):
        if "function" in code and "onlyOwner" not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if "function" in line and "public" in line:
                    lines[i] = line.replace("public", "public onlyOwner")
                    break
            code = '\n'.join(lines)
        
        return code
    
    def get_stats(self):
        """Get contract statistics"""
        return {
            "version": self.version,
            "healing_count": self.healing_count,
            "vulnerabilities_fixed": self.vulnerabilities_fixed,
            "contract_size": len(self.contract_code),
            "uptime_seconds": round(time.time() - self.creation_time, 2),
            "state_size": len(self.state)
        }

class SecurityScanner:
    """Security vulnerability scanner"""
    
    def scan(self, code):
        """Scan code for vulnerabilities"""
        vulnerabilities = []
        
        if self._check_reentrancy(code):
            vulnerabilities.append({
                "type": "reentrancy",
                "severity": "HIGH",
                "description": "Possible reentrancy attack"
            })
        
        if self._check_overflow(code):
            vulnerabilities.append({
                "type": "overflow",
                "severity": "MEDIUM",
                "description": "Possible integer overflow"
            })
        
        if self._check_access_control(code):
            vulnerabilities.append({
                "type": "access_control",
                "severity": "HIGH",
                "description": "Weak access control"
            })
        
        return vulnerabilities
    
    def _check_reentrancy(self, code):
        patterns = [
            r"\.call\.value\(",
            r"\.send\(",
            r"\.transfer\(",
            r"external.*call"
        ]
        
        for pattern in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        
        return False
    
    def _check_overflow(self, code):
        patterns = [
            r"\+\s*[a-zA-Z_][a-zA-Z0-9_]*",
            r"-\s*[a-zA-Z_][a-zA-Z0-9_]*",
            r"\*\s*[a-zA-Z_][a-zA-Z0-9_]*"
        ]
        
        safe_patterns = [
            r"SafeMath",
            r"require.*>=",
            r"require.*<="
        ]
        
        has_overflow_risk = False
        for pattern in patterns:
            if re.search(pattern, code):
                has_overflow_risk = True
        
        has_protection = False
        for pattern in safe_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                has_protection = True
        
        return has_overflow_risk and not has_protection
    
    def _check_access_control(self, code):
        critical_functions = ["mint", "burn", "pause", "unpause", "withdraw"]
        
        for func in critical_functions:
            if func in code.lower():
                func_pattern = rf"function\s+{func}"
                if re.search(func_pattern, code, re.IGNORECASE):
                    line_with_func = ""
                    lines = code.split('\n')
                    for i, line in enumerate(lines):
                        if func in line.lower() and "function" in line.lower():
                            line_with_func = line
                            break
                    
                    if "onlyOwner" not in line_with_func and "modifier" not in line_with_func:
                        return True
        
        return False

def create_sample_contract():
    """Create sample contract"""
    contract_code = """
contract SelfHealingToken {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
        balances[msg.sender] = 1000000;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function mint(address to, uint256 amount) public {
        balances[to] += amount;
    }
    
    function balanceOf(address addr) public view returns (uint256) {
        return balances[addr];
    }
}
"""
    return contract_code
