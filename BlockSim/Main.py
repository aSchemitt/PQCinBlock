from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics
import csv

if p.model == 3:
    from Models.AppendableBlock.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.AppendableBlock.Transaction import FullTransaction as FT
    from Models.AppendableBlock.Node import Node
    from Models.Incentives import Incentives
    from Models.AppendableBlock.Statistics import Statistics
    from Models.AppendableBlock.Verification import Verification

elif p.model == 2:
    from Models.Ethereum.BlockCommit import BlockCommit
    from Models.Ethereum.Consensus import Consensus
    from Models.Ethereum.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Ethereum.Node import Node
    from Models.Ethereum.Incentives import Incentives

elif p.model == 1:
    from Models.Bitcoin.BlockCommit import BlockCommit
    from Models.Bitcoin.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Bitcoin.Node import Node
    from Models.Incentives import Incentives

elif p.model == 0:
    from Models.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Node import Node
    from Models.Incentives import Incentives

########################################################## Start Simulation ##############################################################


def main():
    # TODO: adicionar a execução baseada no arquivo de resultados
    filename = "entrada.csv"
    try: 
        with open(filename,'r', newline='') as inputs:
            reader = csv.reader(inputs)
            cabecalho = next(reader)
            if cabecalho != ["variant", "mean_verify", "std_verify"]:
                print(f"Aviso: O cabeçalho esperado é 'variant,mean_verify,std_verify', mas foi encontrado: {cabecalho}")
            for line in reader:
                if len(line) == 3:
                    variant = line[0]
                    print(variant)
                    p.variant = variant
                    print(p.variant)
                    try:
                        mean_verify = float(line[1])
                        std_verify = float(line[2])
                        p.mean_verify = mean_verify
                        p.std_verify = std_verify
                    except Exception as e:
                        print(e)
                    try:
                        for i in range(p.Runs):
                            clock = 0  # set clock to 0 at the start of the simulation
                            if p.hasTrans:
                                if p.Ttechnique == "Light":
                                    LT.create_transactions()  # generate pending transactions
                                elif p.Ttechnique == "Full":
                                    FT.create_transactions()  # generate pending transactions

                            Node.generate_gensis_block()  # generate the gensis block for all miners
                            # initiate initial events >= 1 to start with
                            BlockCommit.generate_initial_events()

                            while not Queue.isEmpty() and clock <= p.simTime:
                                next_event = Queue.get_next_event()
                                clock = next_event.time  # move clock to the time of the event
                                BlockCommit.handle_event(next_event)
                                Queue.remove_event(next_event)

                            # for the AppendableBlock process transactions and
                            # optionally verify the model implementation
                            if p.model == 3:
                                BlockCommit.process_gateway_transaction_pools()

                                if i == 0 and p.VerifyImplemetation:
                                    Verification.perform_checks()

                            Consensus.fork_resolution()  # apply the longest chain to resolve the forks
                            # distribute the rewards between the particiapting nodes
                            Incentives.distribute_rewards()
                            # calculate the simulation results (e.g., block statstics and miners' rewards)
                            Statistics.calculate()

                            if p.model == 3:
                                Statistics.print_to_excel(i, True)
                                Statistics.reset()
                            else:
                                ########## reset all global variable before the next run #############
                                Statistics.reset()  # reset all variables used to calculate the results
                                Node.resetState()  # reset all the states (blockchains) for all nodes in the network
                                fname = "results/{0}(Allverify)1day_{1}M_{2}K.xlsx".format(p.variant, p.Bsize/1000000, p.Tn/1000)
                                # print all the simulation results in an excel file
                                Statistics.print_to_excel(fname)
                                fname = "results/{0}(Allverify)1day_{1}M_{2}K.xlsx".format(p.variant, p.Bsize/1000000, p.Tn/1000)
                                # print all the simulation results in an excel file
                                Statistics.print_to_excel(fname)
                                try:
                                    Statistics.print_to_csv()
                                except Exception as e:
                                    print("Error ("+str(e)+") in print csv")
                                Statistics.reset2()  # reset profit results
                    except Exception as e:
                        print("Error ("+str(e)+") in main loop")
    except Exception as e:
        print(e)


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
