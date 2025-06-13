Option Explicit

' Solucionador de Sudoku 9x9 en VBA para Excel
' Resuelve una cuadrícula 9x9 usando backtracking, lee desde la celda activa y colorea las celdas resueltas
' Autor: Oscar Calvo
' Fecha: Marzo de 2022
'
Sub SolveSudoku()
    Dim grid(0 To 8, 0 To 8) As Integer
    Dim original(0 To 8, 0 To 8) As Integer
    Dim startCell As Range
    Dim i As Integer, j As Integer
    
    ' Se establece la celda inicial (parte superior izquierda de la cuadrícula 9x9)
    Set startCell = ActiveCell
    
    ' Lee la cuadrícula de 9x9 de la hoja y guarda el juego original (sin resolver)
    For i = 0 To 8
        For j = 0 To 8
            Dim cellValue As Variant
            cellValue = startCell.Offset(i, j).Value
            If IsNumeric(cellValue) And cellValue >= 1 And cellValue <= 9 Then
                grid(i, j) = Int(cellValue)
                original(i, j) = grid(i, j)
            Else
                grid(i, j) = 0
                original(i, j) = 0
            End If
        Next j
    Next i
    
    ' Resuelve el Sudoku
    If Solve(grid) Then
        ' Vuelve a escribir la cuadrícula resuelta en la hoja de cálculo y colorea las celdas rellenas
        For i = 0 To 8
            For j = 0 To 8
                With startCell.Offset(i, j)
                    .Value = grid(i, j)
                    ' Colorea la celda de color AZUL si estaba originalmente vacia (rellenada por el solucionador)
                    If original(i, j) = 0 Then
                        .Font.Color = vbBlue
                    End If
                End With
            Next j
        Next i
        MsgBox "Sudoku resuelto!", vbInformation
    Else
        MsgBox "No hay solución para este Sudoku :( .", vbExclamation
    End If
End Sub

Private Function Solve(ByRef grid() As Integer) As Boolean
    Dim row As Integer, col As Integer
    
    ' Encuentra una celda vacía
    If Not FindEmptyCell(grid, row, col) Then
        Solve = True ' Sudoku resuelto
        Exit Function
    End If
    
    ' Ensayar numeros de 1 a 9
    Dim num As Integer
    For num = 1 To 9
        If IsSafe(grid, row, col, num) Then
            ' Coloca el número
            grid(row, col) = num
            
            ' Trata de resolver el resto de forma recursiva
            If Solve(grid) Then
                Solve = True
                Exit Function
            End If
            
            ' Si la colocación del numero no da una solución, se retrocede
            grid(row, col) = 0
        End If
    Next num
    
    Solve = False ' No se encuentró una solución
End Function

Private Function FindEmptyCell(ByRef grid() As Integer, ByRef row As Integer, ByRef col As Integer) As Boolean
    For row = 0 To 8
        For col = 0 To 8
            If grid(row, col) = 0 Then
                FindEmptyCell = True
                Exit Function
            End If
        Next col
    Next row
    FindEmptyCell = False
End Function

Private Function IsSafe(ByRef grid() As Integer, ByVal row As Integer, ByVal col As Integer, ByVal num As Integer) As Boolean
    ' Chequea fila (verifica que el número ya exista en la fila)
    Dim i As Integer
    For i = 0 To 8
        If grid(row, i) = num Then
            IsSafe = False
            Exit Function
        End If
    Next i
    
    ' Chequea columna
    Dim j As Integer
    For j = 0 To 8
        If grid(j, col) = num Then
            IsSafe = False
            Exit Function
        End If
    Next j
    
    ' Chequea caja de 3x3
    Dim startRow As Integer, startCol As Integer
    startRow = row - row Mod 3
    startCol = col - col Mod 3
    For i = 0 To 2
        For j = 0 To 2
            If grid(startRow + i, startCol + j) = num Then
                IsSafe = False
                Exit Function
            End If
        Next j
    Next i
    
    IsSafe = True
End Function
