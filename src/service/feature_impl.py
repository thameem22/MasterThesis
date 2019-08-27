import re


class Feature:
    """
        This is a class to store the features for a CSV file.

        Attributes:
            chunks (array): To store all the chunks for future processing.
    """
    chunks = []

    def featureInit(self, dataList):
        """
            This method is initiated  when a CSV file is loaded.

            Parameters:
            dataList (array): To store all the data.
        """
        self.chunks = []
        chunk = []
        for line in dataList:
            if len(line) > 10:
                data = [x.strip() for x in line.split(',')]
                chunk.append(line)
                if data[0] == '*ENTER*':
                    self.chunks.append(chunk)
                    chunk = []

    def calculateFeature(self, choice):
        """
            This method calculates and returns the result for a selected feature.

            Parameters:
            choice (string): The selected feature.

            Returns:
            string: The result of a feature
        """
        if choice == 'Exclamation':
            return self.exclamationDensity()
        elif choice == 'Emoticons':
            return self.emoticonsDensity()
        elif choice == 'UpperCase':
            return self.uppercaseDensity()
        elif choice == 'TypingSpeed':
            return self.typingSpeed()
        elif choice == 'LatencyTime':
            return self.latencyTime()
        elif choice == 'ChunkLength':
            return self.chunkLength()
        elif choice == 'ChunkDuration':
            return self.chunkDuration()
        elif choice == 'TotalTokens':
            return self.totalTokens()
        elif choice == 'BackspaceDensity':
            return self.backspaceDensity()
        elif choice == 'BackspaceTime':
            return self.backspaceTime()
        elif choice == 'Questionmark':
            return self.questionmarkDensity()
        elif choice == 'SuspensionPoint':
            return self.suspensionpointDensity()
        elif choice == 'PointsDensity':
            return self.pointsDensity()
        elif choice == 'CapitalLetter':
            return self.capitalLetterDensity()
        elif choice == 'NonAlphabetic':
            return self.nonalphabeticDensity()

    def renderOutput(self, output, text1, text2):
        """
            This method renders the output for every chunk.

            Parameters:
            output (array): An array of output for every chunk.

            Returns:
            string: The result of a chunk
        """
        result = ""
        index = 1
        for value in output:
            result += text1 + " in chunk " + str(index) + " is " + str(value) + " " + text2 + "\n"
            index += 1
        return result

    def densityCalculation(self, keys):
        """
            This method calculates the density for every chunk which matches a key.

            Parameters:
            keys (array): The list of strings to be checked.

            Returns:
            string: The output of a feature
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] in keys:
                    count += 1
            density = count / (len(chunk))
            density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def exclamationDensityCalc(self):
        keys = []
        keys.append("!")
        return self.densityCalculation(keys)

    def exclamationDensity(self):
        """
            This method calculates the exclamation density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = self.exclamationDensityCalc()
        return self.renderOutput(output, "Density of exclamation", "exclamation keys per chunk")

    def emoticonsDensityCalc(self):
        keys = []
        keys.append(":)")
        keys.append(":(")
        keys.append(":-)")
        keys.append(":-(")
        return self.densityCalculation(keys)

    def emoticonsDensity(self):
        """
            This method calculates the emoticons density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = self.emoticonsDensityCalc()
        return self.renderOutput(output, "Density of emoticons", "emoticon keys per chunk")

    def uppercaseDensityCalc(self):
        """
            This method calculates the uppercase density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            tokens = []
            keys = ""
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '*SPACE*' or data[0] == '*ENTER*':
                    if len(keys) > 0:
                        tokens.append(keys)
                    keys = ""
                else:
                    keys += data[0]

            for token in tokens:
                if token.isupper():
                    count += 1

            density = 0
            if len(tokens) > 0:
                density = count / len(tokens)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def uppercaseDensity(self):
        output = self.uppercaseDensityCalc()
        return self.renderOutput(output, "Density of upper", "upper case keys per chunk")

    def typingSpeedCalc(self):
        """
            This method calculates the average typing speed for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = []
        index = 0
        for chunk in self.chunks:
            initialChunk = chunk[0]
            data = [x.strip() for x in initialChunk.split(',')]
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                continue
            initialTime = userTimestamp

            finalChunk = chunk[-1]
            data = [x.strip() for x in finalChunk.split(',')]
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                continue
            finalTime = userTimestamp

            chunkPair = len(chunk)

            density = 0
            duration = (finalTime - initialTime) / 1000
            if chunkPair > 1:
                density = chunkPair / duration
                density = round(density, 3)
            output.append(density)
            index += 1
        return output

    def typingSpeed(self):
        output = self.typingSpeedCalc()
        return self.renderOutput(output, "Typing speed", "keys per seconds")

    def latencyTimeCalc(self):
        """
            This method calculates the latency time for every chunk.
            Latency time is the time difference between consecutive keys.

            Returns:
            string: The calculated output for every chunk.
        """
        output = []
        index = 0
        for chunk in self.chunks:
            prevTime = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[1].isnumeric():
                    userTimestamp = int(data[1])
                else:
                    continue
                if prevTime == 0:
                    prevTime = userTimestamp
                    continue
                density = userTimestamp - prevTime
                prevTime = userTimestamp
                output.append(density)
            index += 1
        return output

    def latencyTime(self):
        output = self.latencyTimeCalc()
        return self.renderOutput(output, "Latency time", "milliseconds")

    def chunkLengthCalc(self):
        """
            This method calculates the length for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            chunkLength = len(chunk) - 1
            output[index] = chunkLength
            index += 1
        return output

    def chunkLength(self):
        output = self.chunkLengthCalc()
        return self.renderOutput(output, "Length", "keys")

    def chunkDurationCalc(self):
        """
            This method calculates the duration for every chunk.
            The duration is the difference between final and initial chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            initialChunk = chunk[0]
            data = [x.strip() for x in initialChunk.split(',')]
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                continue
            initialTime = userTimestamp

            finalChunk = chunk[-1]
            data = [x.strip() for x in finalChunk.split(',')]
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                continue
            finalTime = userTimestamp
            density = (finalTime - initialTime) / 1000
            output[index] = density
            index += 1
        return output

    def chunkDuration(self):
        output = self.chunkDurationCalc()
        return self.renderOutput(output, "Duration", "seconds")

    def totalTokensCalc(self):
        """
            This method calculates the total tokens for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            keys = ""
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '*SPACE*' or data[0] == '*ENTER*':
                    if len(keys) > 0:
                        count += 1
                    keys = ""
                else:
                    keys += data[0]

            output[index] = count
            index += 1
        return output

    def totalTokens(self):
        output = self.totalTokensCalc()
        return self.renderOutput(output, "Total tokens", "tokens")

    def backspaceDensityCalc(self):
        """
            This method calculates the backspace density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '*BS*':
                    count += 1

            density = 0
            if len(chunk) > 1:
                density = count / (len(chunk) - 1)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def backspaceDensity(self):
        output = self.backspaceDensityCalc()
        return self.renderOutput(output, "Density of backspace", "backspace keys per chunk")

    def backspaceTimeCalc(self):
        """
            This method calculates the backspace time for every chunk.
            Backspace time is the total duration between consecutive backspace keys.

            Returns:
            string: The calculated output for every chunk.
        """
        output = []
        index = 0
        for chunk in self.chunks:
            prevTime = 0
            prevKey = ""
            totalTime = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[1].isnumeric():
                    userTimestamp = int(data[1])
                else:
                    continue
                if data[0] == '*BS*':
                    if prevKey == '*BS*':
                        totalTime += userTimestamp - prevTime

                prevTime = userTimestamp
                prevKey = data[0]
            output.append(totalTime)
            index += 1
        return output

    def backspaceTime(self):
        output = self.backspaceTimeCalc()
        return self.renderOutput(output, "Backspace time ", "milliseconds")

    def questionmarkDensityCalc(self):
        """
            This method calculates the question mark density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '?':
                    count += 1

            density = 0
            if len(chunk) > 1:
                density = count / (len(chunk) - 1)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def questionmarkDensity(self):
        output = self.questionmarkDensityCalc()
        return self.renderOutput(output, "Density of question mark", "question mark keys per chunk")

    def suspensionpointDensityCalc(self):
        """
            This method calculates the suspension point density for every chunk.
            Suspension point is the total number of keys between consecutive points

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            totalCharCount = 0
            densityPointCount = 0
            keys = ""
            density = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '.':
                    if len(keys) > 0:
                        totalCharCount += len(keys)
                        densityPointCount += 1
                    keys = ""
                else:
                    keys += data[0]

            if densityPointCount > 0:
                density = totalCharCount / densityPointCount
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def suspensionpointDensity(self):
        output = self.suspensionpointDensityCalc()
        return self.renderOutput(output, "Density of suspension points", "suspension point keys per chunk")

    def pointsDensityCalc(self):
        """
            This method calculates the points density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0] == '.':
                    count += 1

            density = 0
            if len(chunk) > 1:
                density = count / (len(chunk) - 1)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def pointsDensity(self):
        output = self.pointsDensityCalc()
        return self.renderOutput(output, "Density of points", "point keys per chunk")

    def capitalLetterDensityCalc(self):
        """
            This method calculates the capital letter density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if data[0].isupper():
                    count += 1

            density = 0
            if len(chunk) > 1:
                density = count / (len(chunk) - 1)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def capitalLetterDensity(self):
        output = self.capitalLetterDensityCalc()
        return self.renderOutput(output, "Density of capital letters", "capital letter keys per chunk")

    def nonalphabeticDensityCalc(self):
        """
            This method calculates the non-alphabetic key density for every chunk.

            Returns:
            string: The calculated output for every chunk.
        """
        output = [None] * len(self.chunks)
        index = 0
        for chunk in self.chunks:
            count = 0
            for line in chunk:
                data = [x.strip() for x in line.split(',')]
                if not (re.match("[0-9a-zA-Z\\s.]", data[0]) or data[0] == '*SPACE*' or data[0] == '*BS*'
                        or data[0] == '*ENTER*'):
                    count += 1

            density = 0
            if len(chunk) > 1:
                density = count / (len(chunk) - 1)
                density = round(density, 3)
            output[index] = density
            index += 1
        return output

    def nonalphabeticDensity(self):
        output = self.nonalphabeticDensityCalc()
        return self.renderOutput(output, "Density of non-alphabetic characters",
                                 "non-alphabetic characters keys per chunk")
