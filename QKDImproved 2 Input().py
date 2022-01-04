from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse

class qubit():
	def __init__(self,initial_state):
		if initial_state:
			self.__state = matrix([[0],[1]])
		else:
			self.__state = matrix([[1],[0]])
		self.__measured = False
		self.__H = (1/sqrt(2))*matrix([[1,1],[1,-1]])
		self.__X = matrix([[0,1],[1,0]])
	def show(self):
                aux = ""
                if round(matrix([1,0])*self.__state,2):
                        aux += "{0}|0>".format(str(round(matrix([1,0])*self.__state,2)) if round(matrix([1,0])*self.__state,2) != 1.0 else '')
                if round(matrix([0,1])*self.__state,2):
                        if aux:
                                aux += " + "
                        aux += "{0}|1>".format(str(round(matrix([0,1])*self.__state,2)) if round(matrix([0,1])*self.__state,2) != 1.0 else '')
                if round(matrix([1,1])*self.__state,2):
                        if aux:
                                aux += " + "
                        aux += "{1}|1>".format(str(round(matrix([1,1])*self.__state,2)) if round(matrix([1,1])*self.__state,2) != 1.0 else '')
                if round(matrix([0,0])*self.__state,2):
                        if aux:
                                aux += " + "
                        aux += "{0}|0>".format(str(round(matrix([0,0])*self.__state,2)) if round(matrix([0,0])*self.__state,2) != 1.0 else '')
                return aux
	def measure(self):
		M = 1000000
		m = randint(0,M)
		self.__measured = True
		if m < round(pow(matrix([1,0])*self.__state,2),2)*M:
			return 0
		else:
			return 1
	def hadamard(self):
		self.__state = self.__H*self.__state
	def X(self):
		self.__state = self.__X*self.__state

class quantum_user():
	def __init__(self,name):
		self.name = name
	def send(self,data,basis):
		assert len(data) == len(basis), "Basis and data must be the same length!"
		qubits = list()
		for i in range(len(data)):
			if not basis[i]:
				#Base computacional
				if not data[i]:
					qubits.append(qubit(0))
				else:
					qubits.append(qubit(1))
			else:
				#Base Hadamard
				if not data[i]:
					aux = qubit(0)
				else:
					aux = qubit(1)
				aux.hadamard()
				qubits.append(aux)
		return qubits
	def receive(self,data,basis):
		assert len(data) == len(basis), "Basis and data must be the same length!"
		bits = list()
		for i in range(len(data)):
			if not basis[i]:
				bits.append(data[i].measure())
			else:
				data[i].hadamard()
				bits.append(data[i].measure())
		return bits
def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux

def QKD(N,verbose=False,eve_present=False):
        alice_basis = generate_random_bits(N)
        alice_bits = generate_random_bits(N)
        alice = quantum_user("Alice")
        alice_qubits = alice.send(data=alice_bits,basis=alice_basis)
        if eve_present:
                eve_basis = generate_random_bits(N)
                eve = quantum_user("Eve")
                eve_bits = eve.receive(data=alice_qubits,basis=eve_basis)
                alice_qubits = eve.send(data=eve_bits,basis=eve_basis)
        bob_basis = generate_random_bits(N)
        bob = quantum_user("Bob")
        bob_bits = bob.receive(data=alice_qubits,basis=bob_basis)
        bob_qubits = bob.send(data=bob_bits,basis=bob_basis)
        if eve_present:
                eve_basis = generate_random_bits(N)
                eve = quantum_user("Eve")
                eve_bits = eve.receive(data=alice_qubits,basis=eve_basis)
                alice_qubits = eve.send(data=eve_bits,basis=eve_basis)
        kar_basis = generate_random_bits(N)
        kar = quantum_user("Karthik")
        kar_bits = kar.receive(data=bob_qubits,basis=kar_basis)
        kar_qubits = kar.send(data=kar_bits,basis=kar_basis)
        if eve_present:
                eve_basis = generate_random_bits(N)
                eve = quantum_user("Eve")
                eve_bits = eve.receive(data=alice_qubits,basis=eve_basis)
                alice_qubits = eve.send(data=eve_bits,basis=eve_basis)
        rav_basis = generate_random_bits(N)
        rav = quantum_user("Ravi")
        rav_bits = rav.receive(data=bob_qubits,basis=rav_basis)
        alice_key = list()
        bob_key = list()
        kar_key = list()
        rav_key = list()
        for i in range(N):
                if alice_basis[i] == bob_basis[i]:
                        alice_key.append(alice_bits[i])
                        bob_key.append(bob_bits[i])
                if bob_basis[i] == kar_basis[i]:
                        bob_key.append(bob_bits[i])
                        kar_key.append(kar_bits[i])
                if bob_basis[i] == rav_basis[i]:
                        kar_key.append(bob_bits[i])
                        rav_key.append(rav_bits[i])
        if alice_key != bob_key:
                key = False
                length = None
                print("Encription key mismatch, eve is present.")
        else:
                key = True
                length = len(bob_key)
                print("Successfully exchanged key!")
                print("Key Length: " + str(length))
        if bob_key != kar_key:
                key = False
                length = None
                print("Encription key mismatch, eve is present.")
        else:
                key = True
                length = len(bob_key)
                print("Successfully exchanged key!")
                print("Key Length: " + str(length))
        if bob_key != rav_key:
                key = False
                length = None
                print("Encription key mismatch, eve is present.")
        else:
                key = True
                length = len(bob_key)
                print("Successfully exchanged key!")
                print("Key Length: " + str(length))
        if verbose:
                print("Alice generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in alice_basis))
                input()
                print("Alice generates {0} random bits.".format(str(N)))
                input()
                print(''.join(str(e) for e in alice_bits))
                input()
                print("Alice sends to Bob {0} encoded Qubits.".format(str(N)))
                input()
                aux = ""
                for q in alice_qubits:
                        aux += q.show() + "   "
                print(aux)
                raw_input()
                if eve_present:
                        print("Eve intercepts Qubits!")
                        input()
                        print(''.join(str(e) for e in eve_basis))
                        input()
                        print("Eve's bits.")
                        input()
                        print(''.join(str(e) for e in eve_bits))
                        input()
                print("Bob generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in bob_basis))
                input()
                print("Bob receives and decodes Alice's Qubits.")
                input()
                print(''.join(str(e) for e in bob_bits))
                input()
                print("Alice and Bob interchange basis through Internet and compare their basis.")
                input()
                print("Bob generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in bob_basis))
                input()
                print("Bob generates {0} random bits.".format(str(N)))
                input()
                print(''.join(str(e) for e in bob_bits))
                input()
                print("Bob sends to Karthik {0} encoded Qubits.".format(str(N)))
                input()
                aux = ""
                for q in bob_qubits:
                        aux += q.show() + "   "
                print(aux)
                raw_input()
                if eve_present:
                        print("Eve intercepts Qubits!")
                        input()
                        print(''.join(str(e) for e in eve_basis))
                        input()
                        print("Eve's bits.")
                        input()
                        print(''.join(str(e) for e in eve_bits))
                        input()
                print("karthik generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in kar_basis))
                input()
                print("Karthik receives and decodes Bob's Qubits.")
                input()
                print(''.join(str(e) for e in kar_bits))
                input()
                print("Bob and Karthik interchange basis through Internet and compare their basis.")
                input()
                print("Bob generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in bob_basis))
                input()
                print("Bob generates {0} random bits.".format(str(N)))
                input()
                print(''.join(str(e) for e in bob_bits))
                input()
                print("Bob sends to Ravi {0} encoded Qubits.".format(str(N)))
                input()
                aux = ""
                for q in bob_qubits:
                        aux += q.show() + "   "
                print(aux)
                raw_input()
                if eve_present:
                        print("Eve intercepts Qubits!")
                        input()
                        print(''.join(str(e) for e in eve_basis))
                        input()
                        print("Eve's bits.")
                        input()
                        print(''.join(str(e) for e in eve_bits))
                        input()
                print("Ravi generates {0} random basis.".format(str(N)))
                input()
                print(''.join(str(e) for e in rav_basis))
                input()
                print("Ravi receives and decodes Bob Qubits.")
                input()
                print(''.join(str(e) for e in rav_bits))
                input()
                print("Bob and Ravi interchange basis through Internet and compare their basis.")
                input()
        return key

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='KMB09 QKD demonstration with Python.')
	requiredNamed = parser.add_argument_group('Required arguments')
	optionalNamed = parser.add_argument_group('Optional arguments')
	requiredNamed.add_argument('-q','--qubits', required=True, help='Number of Qubits.')
	optionalNamed.add_argument('-i','--iterate',required=False, help='Number of iterations.')
	optionalNamed.add_argument('-e','--eve', action='store_true',default=False,required=False, help='Is EVE present?')
	optionalNamed.add_argument('-v','--verbose', action='store_true',default=False,required=False, help='Verbose logs.')
	args = parser.parse_args()
	assert int(args.qubits)
	ret = list()
	if args.iterate:
		assert int(args.iterate)
		N = int(args.iterate)
	else:
		N = 1
	for i in range(N):
		print("############# {0} #############".format(str(i)))
		ret.append(QKD(int(args.qubits),verbose=args.verbose,eve_present=args.eve))
		print("###############################".format(str(i)))
	print("############################")
	print("############################")
	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	print("True: {0} <{1}%>".format(ret.count(True),str(t)))
	print("False: {0} <{1}%>".format(ret.count(False),str(u)))
