#!/usr/bin/env python3

import re
import sys

class NameFormatter:
    def rearrange_name(self, fname, lname):
        try:
            full_name = f'{fname} {lname}'
            result = re.search(r'^([\w .-]*), ([\w .-]*)$', full_name)
            if result:
                return '{} {}'.format(result[2], result[1])
            else:
                raise ValueError('Invalid input format. Please provide firstname and lastname separated by a comma.')
        except KeyboardInterrupt:
            return 'Process interrupted by user.'
        except ValueError as ve:
            return f'ValueError: {str(ve)}'
        except Exception as e:
            return f'Error: {str(e)}'

if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            print('Usage:\n\tpython script.py \'firstname\' \'lastname\'')
            sys.exit(1)
        
        fname = sys.argv[1]
        lname = sys.argv[2]
        
        formatter = NameFormatter()
        print(formatter.rearrange_name(fname, lname))
    
    except KeyboardInterrupt:
        print('\nProcess interrupted by user.')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)
