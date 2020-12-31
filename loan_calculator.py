import argparse
import math
import sys


class Loan:

    def __init__(self, principal=0, monthly_pay=0, diff_pay=[],
                 num_months=0, interest=0):
        self.principal = principal
        self.monthly_pay = monthly_pay
        self.diff_pay = diff_pay
        self.num_months = num_months
        self.interest = interest

    def __repr__(self):
        return 'Loan(principal={}, monthly_pay={}, diff_pay={}, \
                num_months={}, interest={})'.format(self.principal,
                                                    self.monthly_pay,
                                                    self.diff_pay,
                                                    self.num_months,
                                                    self.interest)

    def calc_num_months(self):
        """Calculates number of months until repayment (with interest)"""
        i = (self.interest / 100) / 12
        n = math.log((self.monthly_pay / (self.monthly_pay - i
                                          * self.principal)), 1 + i)
        self.num_months = math.ceil(n)
        years = n // 12
        months = n % 12
        if months > 11:
            years += 1
            months = 0
        if years == 0:
            print(f'It will take {months} months to repay this loan!')
        elif years == 1:
            print(f'It will take {years} year and {months} months to '
                  + 'repay this loan!')
        else:
            print(f'It will take {years} years and {months} months to '
                  + 'repay this loan!')

    def calc_annuity_pay(self):
        """Calculates monthly annuity payment"""
        i = (self.interest / 100) / 12
        monthly_pay = self.principal * ((i * (1 + i) ** self.num_months)
                                        / ((1 + i) ** self.num_months - 1))
        self.monthly_pay = math.ceil(monthly_pay)
        print(f'Your annuity payment = {self.monthly_pay}!')

    def calc_principal(self):
        """Calculates loan principal"""
        i = (self.interest / 100) / 12
        self.principal = self.monthly_pay / ((i * (1 + i) ** self.num_months)
                                             / ((1 + i)
                                                ** self.num_months - 1))
        self.principal = round(self.principal)
        print(f'Your loan principal = {self.principal}!')

    def calc_diff_pay(self):
        """Calculates differentiated payments"""
        i = (self.interest / 100) / 12
        for month in range(1, self.num_months + 1):
            diff_pay = ((self.principal / self.num_months) + i
                        * (self.principal - ((self.principal * (month - 1))
                                             / self.num_months)))
            diff_pay = math.ceil(diff_pay)
            self.diff_pay.append(diff_pay)
            print(f'Month {month}: payment is {diff_pay}')
        print('')

    def calc_overpayment(self, type):
        if type == 'annuity':
            overpayment = ((self.monthly_pay * self.num_months)
                           - self.principal)
            print(f'Overpayment = {overpayment}')
        elif type == 'diff':
            overpayment = sum(self.diff_pay) - self.principal
            print(f'\nOverpayment = {overpayment}')


def main():
    # Parse and validate arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('--type', choices=['annuity', 'diff'],
                        help='Specify payment type: annuity or diff.')
    parser.add_argument('--payment', help='Specify monthly payment amount.')
    parser.add_argument('--principal', help='Specify loan principal.')
    parser.add_argument('--periods', help='Number of months to repay loan.')
    parser.add_argument('--interest', help='Specify interest rate')

    args = parser.parse_args()

    if len(sys.argv) < 5:
        print('Incorrect parameters')
        quit()
    elif args.type != 'diff' and args.type != 'annuity':
        print('Incorrect parameters')
        quit()
    elif args.payment and args.type == 'diff':
        print('Incorrect parameters')
        quit()

    # Create a loan instance and process parsed arguments
    loan = Loan()
    if args.type == 'annuity':
        if args.principal and args.payment and args.interest:
            loan.principal = float(args.principal)
            loan.monthly_pay = float(args.payment)
            loan.interest = float(args.interest)
            loan.calc_num_months()
            loan.calc_overpayment(args.type)
        elif args.principal and args.periods and args.interest:
            loan.principal = float(args.principal)
            loan.num_months = float(args.periods)
            loan.interest = float(args.interest)
            loan.calc_annuity_pay()
            loan.calc_overpayment(args.type)
        elif args.payment and args.periods and args.interest:
            loan.monthly_pay = float(args.payment)
            loan.num_months = float(args.periods)
            loan.interest = float(args.interest)
            loan.calc_principal()
            loan.calc_overpayment(args.type)
    elif args.type == 'diff':
        loan.principal = float(args.principal)
        loan.num_months = int(args.periods)
        loan.interest = float(args.interest)
        loan.calc_diff_pay()
        loan.calc_overpayment(args.type)


if __name__ == '__main__':
    main()
