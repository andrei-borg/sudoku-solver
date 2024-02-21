import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN

from sudoku_solver import SUDOKU_BOARD, find_empty_location, is_valid

class SudokuVisualizer:
    def __init__(self, sudoku_board=None, window_size=600, grid_size=9):
        self.sudoku_board = sudoku_board
        self.window_size = window_size
        self.grid_size = grid_size
        self.cell_size = self.window_size // self.grid_size
        self.message = None
        self.message_timer = 0

        pygame.init()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)

        self.original_board = [row[:] for row in self.sudoku_board]  # Copy of the original board
        
        self.selected_cell = None
        self.input_number = None

        # Create window
        self.window = pygame.display.set_mode((self.window_size, self.window_size + 50))
        pygame.display.set_caption("Sudoku")

        self.clock = pygame.time.Clock()

        self.running = True
        self.solving = False

        # Buttons
        self.solve_button_rect = pygame.Rect(10, self.window_size + 10, 100, 30)
        self.solve_button_color = (150, 150, 255)
        self.quit_button_rect = pygame.Rect(120, self.window_size + 10, 100, 30)
        self.quit_button_color = (255, 150, 150)
        self.reset_button_rect = pygame.Rect(230, self.window_size + 10, 100, 30)
        self.reset_button_color = (0, 255, 0)

    def draw_buttons(self):
        pygame.draw.rect(self.window, self.solve_button_color, self.solve_button_rect)
        pygame.draw.rect(self.window, self.quit_button_color, self.quit_button_rect)
        pygame.draw.rect(self.window, self.reset_button_color, self.reset_button_rect)

        font = pygame.font.Font(None, 24)
        solve_text = font.render("Solve", True, self.BLACK)
        quit_text = font.render("Quit", True, self.BLACK)
        reset_text = font.render("Reset", True, self.BLACK)

        solve_text_rect = solve_text.get_rect(center=self.solve_button_rect.center)
        quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        reset_text_rect = reset_text.get_rect(center=self.reset_button_rect.center)

        self.window.blit(solve_text, solve_text_rect)
        self.window.blit(quit_text, quit_text_rect)
        self.window.blit(reset_text, reset_text_rect)

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            pygame.draw.line(self.window, self.BLACK, (0, i * self.cell_size), (self.window_size, i * self.cell_size), 2)
            pygame.draw.line(self.window, self.BLACK, (i * self.cell_size, 0), (i * self.cell_size, self.window_size), 2)

        # Draw bold separative lines around each 3x3 box
        for i in range(0, self.window_size, 3 * self.cell_size):
            pygame.draw.line(self.window, self.BLACK, (i, 0), (i, self.window_size), 3)
            pygame.draw.line(self.window, self.BLACK, (0, i), (self.window_size, i), 3)

    def draw_numbers(self):
        font = pygame.font.Font(None, 36)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.sudoku_board[i][j] != 0:
                    text = font.render(str(self.sudoku_board[i][j]), True, self.BLACK)
                    text_rect = text.get_rect(center=(j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2))
                    self.window.blit(text, text_rect)
            
        # Draw error pop-up message if it exists
        if self.message:
            message_rect = self.message.get_rect(center=(self.window_size // 2, self.window_size // 2))
            self.window.blit(self.message, message_rect)
        
        # Update the timer and clear the message after 3 seconds
        self.message_timer += 1
        if self.message_timer > 120:
            self.message = None
            self.message_timer = 0

    def draw_selected_cell(self):
        if self.selected_cell is not None:
            pygame.draw.rect(self.window, self.BLUE, (self.selected_cell[1] * self.cell_size, self.selected_cell[0] * self.cell_size, self.cell_size, self.cell_size), 3)

    def solve_sudoku(self):
        empty_location = find_empty_location(self.sudoku_board)

        if empty_location:
            row, col = empty_location
        else:
            return True

        for num in range(1, 10):
            if is_valid(self.sudoku_board, row, col, num):
                self.sudoku_board[row][col] = num

                # Clear the window before redrawing
                self.window.fill((255, 255, 255))

                self.draw_grid()
                self.draw_numbers()
                self.draw_buttons()
                pygame.display.flip()
                pygame.event.pump()
                pygame.time.delay(10)  # Add a delay for visualization

                # Try to solve the rest of the Sudoku recursively
                if self.solve_sudoku():
                    return True

                # If the placement doesn't lead to a solution, backtrack
                self.sudoku_board[row][col] = 0

                # Clear the window before redrawing
                self.window.fill((255, 255, 255))

                self.draw_grid()
                self.draw_numbers()
                self.draw_buttons()
                pygame.display.flip()
                pygame.event.pump()
                pygame.time.delay(10)  # Add a delay for visualization

        # No number valid, trigger backtracking
        return False

    def reset_board(self):
        self.sudoku_board = [row[:] for row in self.original_board]  # Copy

    def run(self):
        while self.running:
            self.window.fill(self.WHITE)

            self.draw_grid()
            self.draw_numbers()
            self.draw_buttons()
            self.draw_selected_cell()

            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Selected cell
                    row = y // self.cell_size
                    col = x // self.cell_size

                    # Check if the mouse click is within the grid boundaries
                    if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                        self.selected_cell = (row, col)

                    # Check buttons
                    if self.solve_button_rect.collidepoint(x, y) and not self.solving:
                        self.solving = True
                        if not self.solve_sudoku():
                            self.message = pygame.font.Font(None, 36).render("Unable to solve. Check your input!", True, self.RED)
                        self.solving = False

                        # Reset selected cell and input number after solving
                        self.selected_cell = None
                        self.input_number = None

                    elif self.quit_button_rect.collidepoint(x, y):
                        self.running = False

                    elif self.reset_button_rect.collidepoint(x, y):
                        self.reset_board()
                
                # Number key press
                if event.type == KEYDOWN:
                    row, col = self.selected_cell
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9) and self.selected_cell is not None and not self.solving:
                        self.input_number = int(pygame.key.name(event.key))
                        
                        # Check if input number is valid
                        if is_valid(self.sudoku_board, row, col, self.input_number):
                            self.sudoku_board[row][col] = self.input_number

                    # Remove number if '0' is pressed
                    elif event.key == pygame.K_0 and self.selected_cell is not None and not self.solving:
                        self.sudoku_board[row][col] = 0

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    sudoku_visualizer = SudokuVisualizer(sudoku_board=SUDOKU_BOARD)
    sudoku_visualizer.run()
