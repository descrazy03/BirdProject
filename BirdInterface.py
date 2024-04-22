from BirdData import Data


class Interface:
    def __init__(self):
        self.data = Data()

    def instructions(self):
        print('Commands:')
        print('[1] View Most Frequent Locations')
        print('[2] Search By Neighborhood')
        print('[3] Search By Season')
        print('[4] Show Distribution Map')
        print('[0] Exit')

    def most_overall(self):
        print('These are where the parrots are seen most throughout San Francisco!')
        print()
        locs = self.data.most_freq_loc()
        for loc in locs:
            print(f'Location: (Latitude: {loc[1]}, Longitude: {loc[2]})\nNeighborhood: {loc[0]}')
            print()

    def search_neighborhood(self):
        n = self.data.print_neighborhoods()
        for i in n:
            print(i)
        print()
        print("Above is a list of the neighborhoods you can choose from. Be careful! Neighborhoods are case-sensitve and must be spelled correctly.")
        print()

        location = input('Which neighborhood? ')

        if location not in n:
            print('Not a valid neighborhood!')
            print()
        else:
            amount = self.data.no_in_neighborhood(location)
            most_freq_loc = self.data.most_at_location(location)
            print(f"There's been {amount} sighting(s) in the {location} area and have been most spotted at coordinates [Latitude: {most_freq_loc[1]}, Longitude: {most_freq_loc[2]}]")
            print()
            print(f'About {self.data.percent_of_sightings(location):.2f}% of all sightings have been in the {location} area.')

    def search_season(self):
        print('See where the parrots hangout most frequently during specific seasons!')
        print('Type in one of the following seasons to search:')
        print('"winter" === December, January, and February')
        print('"spring" === March, April, and May')
        print('"summer" === June, July, and August')
        print('"fall" === September, October, November')
        print()
        
        season = input('Which season? ')
        print()
        if season.lower() in ['winter', 'summer', 'spring', 'fall']:
            locs = self.data.by_season(season.lower())
            print(f'These are where the birds are most seen during {season.lower()}:')
            print()
            for loc in locs[0]:
                print(f'Location: (Latitude: {loc[1]}, Longitude: {loc[2]})\nNeighborhood: {loc[0]}')
                print()
            print(f'During the {season} seasons, there were {self.data.by_season(season)[1]} sightings of the parrots, which is about {self.data.by_season(season)[2]:.2f}% of all sightings.')

        else:
            print('Not a valid season!')

    def execute(self):
        print()
        print('Hello! Welcome to the SF Parrot Watch!')
        print()
        while True:
            self.instructions()
            print()
            command = input("Command Number: ")
            print()
            if command == "0":
                print('Thank you! Have a wonderful day!')
                break
            if command == '1':
                self.most_overall()
            if command == '2':
                self.search_neighborhood()
            if command == '3':
                self.search_season()
            if command == '4':
                self.data.neighborhood_distribution()




if __name__ == '__main__':
    ui = Interface()
    ui.execute()
    
