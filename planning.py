###=================================================
# This file is where you need to create a plan to reach the goal state from the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State

class Plan:

    def __init__(self, initial_state_blocks, goal_state_blocks):
        """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
        self.initial_state = initial_state_blocks
        self.goal_state = goal_state_blocks
        self.current_state = initial_state_blocks
        self.num_steps = 0

    #***=========================================
    # First implement all the operators
    # I implemented two operators to give you guys an example
    # Please implement the remainder of the operators
    #***=========================================

    def CLEAR(self, block):
        if block.above != None:
            return False
        return True
    
    def AIR(self, block):
        if block.on == None and block.above == None:
            return True
        return False
    
    #the search here might be redundant    
    def ON(self, block1, block2):
        if block1.on == block2:
            return True
        else:
            return False
    

    #pickup a block from the table
    def pickup(self, block):
        if block.above == None and not block.air:
            block.air = True
            block.on = None
            

    def putdown(self, block):
        """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block.air:
            block.on = table
            block.above = None
            block.air = False

    #put block1 on top of block2
    def stack(self, block1, block2):
        if block1.air and block2.above == None:
            block1.on = block2
            block1.air = False
            block1.above = None
            block2.above = block1

    #unstack block1 from block2 and have it in the air
    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        # if block1 is clear it is safe to unstack
        if block1.above == None and not block1.air:

            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.air = True
            block1.on = None
            block2.above = None

    def move(self):
        print("ROBOT'S HAND MOVING")
    # ***=========================================
    # After you implement all the operators
    # The next step is to implement the actual plan.
    # Please fill in the sample plan to output the appropriate steps to reach the goal
    # ***=========================================

    def propositionalize(self):
        #write the five necessary conditions (each one defining where a block is sitting) as booleans
        condition_list = []
        for i in range(5):
            #the list of tuples is representing the ON relation in this form: (block1 id, id of block object on which block1 is sitting)
            condition_list.append((self.goal_state[i+1].id,self.goal_state[i+1].on.id))
        return condition_list


    def decompose(self):
        conditions = self.propositionalize()
        decomposed_conditions = []
        next_level = []
        cur_level_tuples = []
        i=0
        for j in range(5):
            tuple = conditions[i]
            if(tuple[1]=="table"):
                cur_level_tuples.append(tuple)
                next_level.append(tuple[0])
                conditions.remove(tuple)
            else: i+=1
        decomposed_conditions.append(cur_level_tuples)
        while len(conditions)!= 0:
            new_next_level = []
            cur_level_tuples = []
            i=0
            for j in range(len(conditions)):
                tuple = conditions[i]
                if(tuple[1] in next_level):
                    cur_level_tuples.append(tuple)
                    new_next_level.append(tuple[0])
                    conditions.remove(tuple)
                else: i+=1
            decomposed_conditions.append(cur_level_tuples)
            next_level = new_next_level
        return decomposed_conditions
    
    def free_block(self,block):
        if self.CLEAR(block):
            return
        else:
            block_above = block.above
            self.free_block(block_above)
            action = f"unstack {block_above.id} from {block.id}"
            self.move()
            self.unstack(block_above,block)
            self.num_steps += 1
            State.display(self.current_state, message=action)
            action = f"put down {block_above.id} on table"
            self.move()
            self.putdown(block_above)
            self.num_steps += 1
            State.display(self.current_state, message=action)
            return

    def execute_plan(self):
        #write the goal state as a conjuction of ground fluents and divide up the goals
        table = State.find(self.current_state, "table")
        decomposed_goals = self.decompose()
        table_level = decomposed_goals[0]
        decomposed_goals.pop(0)
        for literal in table_level:
            blockId= literal[0]
            block = State.find(self.current_state, blockId)
            if not self.ON(block,table):
                self.free_block(block)
                #we unstack it because if it were on the table, we would not go into the body of the if statement
                action = f"unstack {blockId} from {block.on.id}"
                self.move()
                self.unstack(block, block.on)
                self.num_steps += 1
                State.display(self.current_state, message=action)
                action = f"put down {blockId} on table"
                self.move()
                self.putdown(block)
                self.num_steps += 1
                State.display(self.current_state, message=action)
        #in first level we stack on top of blocks on table, then on top of these, etc. We go row by row.
        for level in decomposed_goals:
            for literal in level:
                blockId = literal[0]
                destination_blockId = literal[1]
                block = State.find(self.current_state, blockId)
                destination_block = State.find(self.current_state, destination_blockId)
                if not self.ON(block,destination_block):
                    self.free_block(block)
                    self.free_block(destination_block)
                    if self.ON(block, table):
                        action = f"pick up {blockId} from table"
                        self.move()
                        self.pickup(block)
                        self.num_steps += 1
                        State.display(self.current_state, message=action)
                    else:
                        action = f"unstack {blockId} from {block.on}"
                        self.move()
                        self.unstack(block, block.on)
                        self.num_steps += 1
                        State.display(self.current_state, message=action)
                    #now we just stack because all blocks that should be on the table are already there
                    action = f"stack {blockId} on {destination_blockId}"
                    self.move()
                    self.stack(block,destination_block)
                    self.num_steps += 1
                    State.display(self.current_state, message=action)
        print(f"NUMBER OF STEPS TAKEN BY THE ROBOT: {self.num_steps} (moving robot's hand not included as a step)")
        return self.num_steps
