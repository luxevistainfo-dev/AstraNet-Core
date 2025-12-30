# ai/smart_contract_checker.py

import re
import ast
import json
from datetime import datetime

class SmartContractValidator:
    def __init__(self, config_file="contract_rules.json"):
        self.forbidden_patterns = [
            r'eval\s*\(', r'exec\s*\(', r'compile\s*\(',
            r'__import__\s*\(', r'open\s*\(', r'file\s*\(',
            r'subprocess\.', r'os\.system\s*\(', r'pickle\.loads',
            r'breakpoint\s*\(', r'globals\s*\(', r'locals\s*\(',
            r'__builtins__', r'__dict__\.', r'__code__',
            r'while\s+True\s*:', r'for\s+.*\s+in\s+.*\s*:.*while',
        ]
        
        self.warning_patterns = [
            r'time\.sleep\s*\(', r'random\.', r'input\s*\(',
            r'while\s+.*:', r'for\s+.*:',
            r'recursive', r'self\.\w+\s*\(.*\)\s*:\s*self\.\w+'
        ]
        
        self.safe_templates = self.load_templates()
        self.config_file = config_file
        self.validation_log = []
        
        print(f"[CONTRACT] Validator initialized with {len(self.safe_templates)} templates")
    
    def load_templates(self):
        """Load safe contract templates"""
        templates = {
            'token_standard': """
class TokenContract:
    def __init__(self, owner, total_supply):
        self.owner = owner
        self.total_supply = total_supply
        self.balances = {owner: total_supply}
    
    def transfer(self, sender, receiver, amount):
        if self.balances.get(sender, 0) >= amount:
            self.balances[sender] = self.balances.get(sender, 0) - amount
            self.balances[receiver] = self.balances.get(receiver, 0) + amount
            return True
        return False
    
    def balance_of(self, address):
        return self.balances.get(address, 0)
""",
            'voting_contract': """
class VotingContract:
    def __init__(self, admin, candidates):
        self.admin = admin
        self.candidates = candidates
        self.votes = {candidate: 0 for candidate in candidates}
        self.voters = set()
    
    def vote(self, voter, candidate):
        if voter not in self.voters and candidate in self.candidates:
            self.voters.add(voter)
            self.votes[candidate] += 1
            return True
        return False
    
    def get_results(self):
        return self.votes
""",
            'escrow_contract': """
class EscrowContract:
    def __init__(self, buyer, seller, amount, arbiter):
        self.buyer = buyer
        self.seller = seller
        self.amount = amount
        self.arbiter = arbiter
        self.released = False
    
    def release_to_seller(self):
        if not self.released:
            self.released = True
            return {"to": self.seller, "amount": self.amount}
        return None
    
    def refund_to_buyer(self):
        if not self.released:
            self.released = True
            return {"to": self.buyer, "amount": self.amount}
        return None
"""
        }
        return templates
    
    def validate_contract(self, contract_code, contract_name="Unknown"):
        """Main validation function"""
        print(f"\n[CONTRACT] Validating: {contract_name}")
        
        result = {
            "contract_name": contract_name,
            "timestamp": datetime.now().isoformat(),
            "safe": True,
            "issues": [],
            "warnings": [],
            "suggestions": [],
            "template_match": None,
            "complexity_score": 0,
            "security_score": 100
        }
        
        # Check 1: Basic syntax
        syntax_issues = self.check_syntax(contract_code)
        if syntax_issues:
            result["issues"].extend(syntax_issues)
            result["safe"] = False
        
        # Check 2: Security patterns
        security_issues = self.check_security_patterns(contract_code)
        if security_issues:
            result["issues"].extend(security_issues)
            result["safe"] = False
        
        # Check 3: Warning patterns
        warnings = self.check_warning_patterns(contract_code)
        if warnings:
            result["warnings"].extend(warnings)
        
        # Check 4: Template matching
        template_match = self.match_template(contract_code)
        result["template_match"] = template_match
        
        # Check 5: Complexity analysis
        complexity = self.analyze_complexity(contract_code)
        result["complexity_score"] = complexity
        if complexity > 50:
            result["warnings"].append(f"High complexity score: {complexity}")
        
        # Check 6: Gas estimation (simulated)
        gas_estimate = self.estimate_gas(contract_code)
        if gas_estimate > 1000000:
            result["warnings"].append(f"High gas estimate: {gas_estimate}")
        
        # Calculate security score
        result["security_score"] = self.calculate_security_score(result)
        
        # Generate suggestions
        result["suggestions"] = self.generate_suggestions(result)
        
        # Log validation
        self.validation_log.append(result)
        self.save_validation_log()
        
        return result
    
    def check_syntax(self, code):
        """Check Python syntax"""
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
        except Exception as e:
            issues.append(f"Code parsing error: {e}")
        
        return issues
    
    def check_security_patterns(self, code):
        """Check for forbidden patterns"""
        issues = []
        
        for pattern in self.forbidden_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line = code[:match.start()].count('\n') + 1
                issues.append(f"Line {line}: Forbidden pattern '{match.group()}' found")
        
        return issues
    
    def check_warning_patterns(self, code):
        """Check for warning patterns"""
        warnings = []
        
        for pattern in self.warning_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line = code[:match.start()].count('\n') + 1
                warnings.append(f"Line {line}: Warning pattern '{match.group()}' found")
        
        # Check for infinite loop patterns
        if self.detect_potential_infinite_loop(code):
            warnings.append("Potential infinite loop detected")
        
        return warnings
    
    def detect_potential_infinite_loop(self, code):
        """Simple infinite loop detection"""
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if 'while True:' in line or 'while 1:' in line:
                # Check if there's a break in the loop
                loop_body = '\n'.join(lines[i+1:i+20])
                if 'break' not in loop_body and 'return' not in loop_body:
                    return True
        return False
    
    def match_template(self, code):
        """Match against known safe templates"""
        best_match = None
        best_score = 0
        
        for template_name, template_code in self.safe_templates.items():
            similarity = self.calculate_similarity(code, template_code)
            if similarity > best_score:
                best_score = similarity
                best_match = template_name
        
        return {
            "template": best_match,
            "confidence": round(best_score * 100, 1),
            "is_standard": best_score > 0.6 if best_match else False
        }
    
    def calculate_similarity(self, code1, code2):
        """Calculate similarity between two code snippets"""
        # Simple token-based similarity
        tokens1 = set(re.findall(r'\b\w+\b', code1))
        tokens2 = set(re.findall(r'\b\w+\b', code2))
        
        if not tokens1 or not tokens2:
            return 0
        
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0
    
    def analyze_complexity(self, code):
        """Analyze code complexity"""
        try:
            tree = ast.parse(code)
            complexity = 0
            
            for node in ast.walk(tree):
                # Count control structures
                if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                    complexity += 1
                # Count function definitions
                elif isinstance(node, ast.FunctionDef):
                    complexity += 2
            
            return int(complexity * 10)
        except:
            return 0
    
    def estimate_gas(self, code):
        """Estimate gas consumption (simplified)"""
        complexity = self.analyze_complexity(code)
        
        # Base gas for contract
        gas = 21000
        
        # Add for loops
        loop_count = len(re.findall(r'\b(for|while)\b', code))
        gas += loop_count * 5000
        
        # Add for function calls
        func_count = len(re.findall(r'def\s+\w+', code))
        gas += func_count * 10000
        
        return gas
    
    def calculate_security_score(self, result):
        """Calculate security score (0-100)"""
        score = 100
        
        # Deduct for issues
        score -= len(result["issues"]) * 15
        
        # Deduct for warnings
        score -= len(result["warnings"]) * 5
        
        # Deduct for high complexity
        if result["complexity_score"] > 50:
            score -= 10
        
        # Bonus for template match
        if result["template_match"]["is_standard"]:
            score += 10
        
        return max(0, min(100, score))
    
    def generate_suggestions(self, result):
        """Generate improvement suggestions"""
        suggestions = []
        
        if result["issues"]:
            suggestions.append("Fix all security issues before deployment")
        
        if result["complexity_score"] > 50:
            suggestions.append("Consider simplifying the contract logic")
        
        if result["template_match"]["confidence"] < 60:
            suggestions.append("Follow standard contract templates for security")
        
        if not result["issues"] and result["security_score"] > 80:
            suggestions.append("Contract looks good! Ready for deployment")
        
        return suggestions
    
    def save_validation_log(self):
        """Save validation log to file"""
        try:
            with open("contract_validations.json", 'w') as f:
                json.dump(self.validation_log[-50:], f, indent=2)
        except Exception as e:
            print(f"[ERROR] Saving validation log: {e}")
    
    def print_validation_report(self, result):
        """Print a formatted validation report"""
        print("\n" + "="*60)
        print(f"CONTRACT VALIDATION REPORT: {result['contract_name']}")
        print("="*60)
        
        print(f"\n📊 SCORES:")
        print(f"  Security Score: {result['security_score']}/100")
        print(f"  Complexity: {result['complexity_score']}/100")
        print(f"  Template Match: {result['template_match']['template']} "
              f"({result['template_match']['confidence']}% confidence)")
        
        if result['issues']:
            print(f"\n❌ CRITICAL ISSUES ({len(result['issues'])}):")
            for issue in result['issues']:
                print(f"  • {issue}")
        
        if result['warnings']:
            print(f"\n⚠️  WARNINGS ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"  • {warning}")
        
        if result['suggestions']:
            print(f"\n💡 SUGGESTIONS:")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion}")
        
        print(f"\n{'✅ SAFE TO DEPLOY' if result['safe'] else '❌ DO NOT DEPLOY'}")
        print("="*60)

# Test function
def test_contract_validator():
    print("\nTesting SmartContractValidator...")
    
    validator = SmartContractValidator()
    
    # Test 1: Safe token contract
    safe_contract = """
class MyToken:
    def __init__(self, owner):
        self.owner = owner
        self.balances = {owner: 1000}
    
    def transfer(self, to, amount):
        if self.balances.get(self.owner, 0) >= amount:
            self.balances[self.owner] -= amount
            self.balances[to] = self.balances.get(to, 0) + amount
            return True
        return False
"""
    
    print("\n=== Test 1: Safe Contract ===")
    result1 = validator.validate_contract(safe_contract, "MyToken")
    validator.print_validation_report(result1)
    
    print("\n✅ Contract validator test completed!")

if __name__ == "__main__":
    test_contract_validator()
