import plotly.graph_objects as go
import copy

class cube:

    def __init__(self, corners_list = []):

        if len(corners_list) == 0:
            self.corners = [
                [1,0],
                [2,0],
                [3,0],
                [4,0],
                [5,0],
                [6,0],
                [7,0]
            ]

        else:
            self._check_corners(corners_list)
            self.corners = corners_list

    def _check_corners(self, corners_list):
        if len(corners_list) != 7:
            raise ValueError("The corners list must have 7 elements!")
        else:
            orientation_sum = 0
            for corner in corners_list:
                if len(corner) != 2:
                    raise ValueError("Each corner must have piece and orientation information (size must be 2)!")
                else:
                    orientation_sum += corner[1]

            mod3_orientation_sum = orientation_sum % 3
            if mod3_orientation_sum != 0:
                raise ValueError("The orientations must add 0 mod 3")

    def _right_move(self):
        c1 = self.corners[0]

        c2 = self.corners[2]
        c2[1] = (c2[1] + 1) % 3

        c3 = self.corners[5]
        c3[1] = (c3[1] - 1) % 3

        c4 = self.corners[3]
        c5 = self.corners[4]

        c6 = self.corners[6]
        c6[1] = (c6[1] + 1) % 3

        c7 = self.corners[1]
        c7[1] = (c7[1] - 1) % 3

        self.corners = [c1, c2, c3, c4, c5, c6, c7]

    def _up_move(self):
        c1 = self.corners[3]
        c2 = self.corners[0]
        c3 = self.corners[1]
        c4 = self.corners[2]
        c5 = self.corners[4]
        c6 = self.corners[5]
        c7 = self.corners[6]

        self.corners = [c1, c2, c3, c4, c5, c6, c7]

    def _front_move(self):
        c1 = self.corners[0]
        c2 = self.corners[1]

        c3 = self.corners[3]
        c3[1] = (c3[1] + 1) % 3

        c4 = self.corners[4]
        c4[1] = (c4[1] - 1) % 3

        c5 = self.corners[5]
        c5[1] = (c5[1] + 1) % 3

        c6 = self.corners[2]
        c6[1] = (c6[1] - 1) % 3

        c7 = self.corners[6]

        self.corners = [c1, c2, c3, c4, c5, c6, c7]

    def show_current_state(self):
        print(self.corners)

    def make_move(self, face, times = 1):
        face = face.upper()
        for i in range(times):
            if face == 'R':
                self._right_move()
            elif face == 'U':
                self._up_move()
            elif face == 'F':
                self._front_move()
            else:
                print("Invalid face name!")
                break

    def is_equal(self, other_cube):
        if self.corners == other_cube.corners:
            return True
        else:
            return False
        
    def copy(self):
        list_of_original_corners = copy.deepcopy(self.corners)
        cube_copy = cube(list_of_original_corners)
        return cube_copy
    
    def is_in(self, cube_list):
        for cube_state in cube_list:
            if self.is_equal(cube_state):
                return True
            
        return False
    
    def get_colors(self, corner):
        color_list = []

        # Yellow or white
        if corner[0] in [5,6,7]:
            color_list.append('white')
        else:
            color_list.append('yellow')

        # Red or orange
        if corner[0] in [1,4,5]:
            color_list.append('orange')
        else:
            color_list.append('red')

        # Green or blue
        if corner[0] in [1,2,7]:
            color_list.append('green')
        else:
            color_list.append('blue')

        if corner[0] in [2,4,6]:
            color_list = [color_list[0], color_list[2], color_list[1]]

        if corner[1] == 1:
            color_list = [color_list[2], color_list[0], color_list[1]]
        elif corner[1] == 2:
            color_list = [color_list[1], color_list[2], color_list[0]]

        return color_list

    def plot_current_state(self):
        # Inform the camera start position
        layout = go.Layout(
                scene=dict(
                    camera=dict(
                        eye=dict(x=1.8, y=0.8, z=0.9)
                    )
                )
            )

        fig = go.Figure(layout=layout)

        # Add fixed piece
        fig.add_trace(
                go.Mesh3d(
                    # 8 vertices of a cube
                    x=[0,  0, -1, -1,  0,  0, -1, -1],
                    y=[0, -1, -1,  0,  0, -1, -1,  0],
                    z=[0,  0,  0,  0, -1, -1, -1, -1],
                    facecolor = ['white', 'white', 'orange', 'orange', 'green', 'green'],
                    # i, j and k give the vertices of triangles
                    i = [6, 6, 6, 6, 6, 6],
                    j = [4, 4, 1, 1, 3, 3],
                    k = [5, 7, 2, 5, 7, 2],
                    name='y',
                    showscale=False
                )
            )

        x_signs=[-1, -1,  1,  1,  1,  1, -1]
        y_signs=[-1,  1,  1, -1, -1,  1,  1]
        z_signs=[ 1,  1,  1,  1, -1, -1, -1]

        for i in range(7):
            corner = self.corners[i]
            corner_list = self.get_colors(corner)

            if i in [1,3,5]:
                corner_list = [corner_list[0], corner_list[2], corner_list[1]]
            
            x_value = x_signs[i]
            y_value = y_signs[i]
            z_value = z_signs[i]
            fig.add_trace(
                go.Mesh3d(
                    # 8 vertices of a cube
                    x=[0,       0, x_value, x_value,       0,       0, x_value, x_value],
                    y=[0, y_value, y_value,       0,       0, y_value, y_value,       0],
                    z=[0,       0,       0,       0, z_value, z_value, z_value, z_value],
                    facecolor = [corner_list[0], corner_list[0], corner_list[1], corner_list[1], corner_list[2], corner_list[2]],
                    # i, j and k give the vertices of triangles
                    i = [6, 6, 6, 6, 6, 6],
                    j = [4, 4, 1, 1, 3, 3],
                    k = [5, 7, 2, 5, 7, 2],
                    name='y',
                    showscale=False
                )
            )

        fig.update_layout(scene=dict(xaxis=dict(title = '', showticklabels=False)))
        fig.update_layout(scene=dict(yaxis=dict(title = '', showticklabels=False)))
        fig.update_layout(scene=dict(zaxis=dict(title = '', showticklabels=False)))

        fig.show()

    def get_integer(self):
        list_of_lists = self.corners
        # Concatenate the inner lists into a single list of integers
        flattened_list = [item for sublist in list_of_lists for item in sublist]
        # Convert the list of integers into a single integer (optional)
        resulting_integer = int(''.join(map(str, flattened_list)))

        return resulting_integer






# my_cube = cube([[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]])
# other_cube = my_cube.copy()
# my_cube.make_move('f', 2)
# my_cube.show_current_state()
# other_cube.show_current_state()
# cube_2 = cube()
# my_cube.show_current_state()
# cube_2.show_current_state()
# print(my_cube.is_equal(cube_2))
# my_cube.make_move('f', 2)
# print(my_cube.is_equal(cube_2))
# my_cube.show_current_state()
# cube_2.show_current_state()

# distance = {}
# distance[0] = [cube()]

# i = 0

# all_cube_states = [cube()]

# while i <= 11:
#     cube_list = []
#     for state in distance[i]:
#         state_copy = state.copy()
#         state_copy.make_move('f', 2)
#         if not state_copy.is_in(all_cube_states):
#             cube_list.append(state_copy)
#             all_cube_states.append(state_copy)

#         state_copy = state.copy()
#         state_copy.make_move('r', 2)
#         if not state_copy.is_in(all_cube_states):
#             cube_list.append(state_copy)
#             all_cube_states.append(state_copy)


#         for j in range(3):
#             state_copy = state.copy()
#             state_copy.make_move('u', j + 1)
#             if not state_copy.is_in(all_cube_states):
#                 cube_list.append(state_copy)
#                 all_cube_states.append(state_copy)
        


#     distance[i + 1] = cube_list
#     i += 1


# print(len(distance[2]))


