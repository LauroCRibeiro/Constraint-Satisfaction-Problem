
'''
Author: Lauro Ribeiro - 2016291 - CCT College
Examiner: David McQuaid

'''

class Variable:

    def __init__(self, variable, domain, neighbours):
        self.variable = variable
        self.domain = domain
        self.neighbours = neighbours
        self.color = None


class ConstraintSatisfactionProblem:

    def backtracking_search(self, csp):
        return self.recursive_backtracking([], csp)

    def recursive_backtracking(self, assignment, csp):
        if self.assignment_complete(assignment, csp):
            return assignment

        unassigned_var = self.get_unassigned_variable(csp, assignment, "DH")

        # Loop through colors of the unassigned variable's domain
        for value in unassigned_var.domain:
            if self.consistent(unassigned_var, value, assignment):
                unassigned_var.color = value
                assignment.append(unassigned_var)
                csp = self.forward_checking(assignment, csp)

                result = self.recursive_backtracking(assignment, csp)
                if result != -1:
                    return result

            if unassigned_var in assignment:
                assignment.remove(unassigned_var)

        # -1 represents failure
        return -1

    def forward_checking(self, assignment, csp):
        unassigned_values = []
        for value in csp:
            if value not in assignment:
                unassigned_values.append(value)

        for value in csp:
            for unassigned_value in unassigned_values:
                if value in unassigned_value.neighbours:
                    for color in value.domain:
                        if not self.consistent(value, color, assignment):
                            value.domain.remove(color)


        return csp

    def consistent(self, unassigned_var, value, assignment):
        assigned_neighbours = []

        for assigned_region in assignment:
            if assigned_region.variable in unassigned_var.neighbours:
                assigned_neighbours.append(assigned_region)

        for assigned_neighbour in assigned_neighbours:
            if value == assigned_neighbour.color:
                return False

        return True

    def is_neighbours(self, region1, region2):
        for neighbour in region1.neighbours:
            if neighbour == region2.variable:
                return True

    def get_unassigned_variable(self, csp, assignment, method):
        # Degree heuristic: Choose the variable involved in most constraints
        if method == "DH":
            neighbours_amount = 0
            selected_region = None

            for region in csp:
                if region not in assignment:
                    if len(region.neighbours) > neighbours_amount:
                        neighbours_amount = len(region.neighbours)
                        selected_region = region

            return selected_region

    def assignment_complete(self, assignment, csp):
        if len(assignment) == len(csp):
            return True

        return False