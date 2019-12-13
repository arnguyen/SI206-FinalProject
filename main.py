import dataProcessor
import visualizations

def menu():
    print('Welcome! Please select an option below.')
    print('(1) Collect and Process Data')
    print('(2) View Visualizations')
    print('(3) Exit')
    usr_response = input('Please select a number. [1-3]')
    return usr_response

def main():
    usr_response = menu()
    if usr_response == '1':
        print('')
        dataProcessor.main()
    elif usr_response == '2':
        print('')
        visualizations.main()
    elif usr_response == '3':
        return
    else: 
        print('\nInvalid response. Please try again.\n')
        return main()
    print('')

    return main()

if __name__ == "__main__":
    main()