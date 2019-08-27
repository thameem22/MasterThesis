import os

import numpy as np
from numpy import mean
from scipy import stats
from scipy.stats import sem
from service.feature_impl import Feature


class StudentsT:
    """
        This is a class to implement the Student's t test for the caller and the receiver.

        Attributes:
            result (string): To store the output.
    """
    result = ''

    def run(self, pathC, pathR):
        """
            This method initiates a feature instance for every file and invokes the t test calculation.

            Parameters:
            pathC (string): The path of the caller.
            pathR (string): The path of the receiver.

            Returns:
            string: The result of the t test between caller and receiver
        """
        self.featureC = []
        entries = os.listdir(pathC)
        for entry in entries:
            print(entry)
            featureC = Feature()
            dataList = self.openFile(pathC, entry)
            featureC.featureInit(dataList)
            self.featureC.append(featureC)

        self.featureR = []
        entries = os.listdir(pathR)
        for entry in entries:
            print(entry)
            featureR = Feature()
            dataList = self.openFile(pathR, entry)
            featureR.featureInit(dataList)
            self.featureR.append(featureR)

        self.featureCalc()
        return self.result

    def openFile(self, path, filename):
        """
            This method opens the file for reading.

            Parameters:
            path (string): The path of the file.
            filename (string): The name of the file.

            Returns:
            array: The list of all the non empty lines from the file
        """
        dataList = []
        file = open(os.path.join(path, filename), "r")

        for line in file:
            if len(line) > 10:
                dataList.append(line)
        return dataList

    def featureCalc(self):
        """
            This method invokes all the feature calculation and t test between caller and receiver.
            The average value is taken for a feature and this value is used for t test.
        """
        self.alpha = 0.05

        outputC = []
        for feature in self.featureC:
            dataList = feature.exclamationDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.exclamationDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "Exclamation")

        outputC = []
        for feature in self.featureC:
            dataList = feature.emoticonsDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.emoticonsDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "Emoticons")

        outputC = []
        for feature in self.featureC:
            dataList = feature.uppercaseDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.uppercaseDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "UpperCase")

        outputC = []
        for feature in self.featureC:
            dataList = feature.typingSpeedCalc()
            if dataList is not None:
                mean = np.mean(dataList)
                outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.typingSpeedCalc()
            if dataList is not None:
                mean = np.mean(dataList)
                outputR.append(mean)
        self.independentTtest(outputC, outputR, "TypingSpeed")

        outputC = []
        for feature in self.featureC:
            dataList = feature.latencyTimeCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.latencyTimeCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "LatencyTime")

        outputC = []
        for feature in self.featureC:
            dataList = feature.chunkLengthCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.chunkLengthCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "ChunkLength")

        outputC = []
        for feature in self.featureC:
            dataList = feature.chunkDurationCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.chunkDurationCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "ChunkDuration")

        outputC = []
        for feature in self.featureC:
            dataList = feature.totalTokensCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.totalTokensCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "TotalTokens")

        outputC = []
        for feature in self.featureC:
            dataList = feature.backspaceDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.backspaceDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "BackspaceDensity")

        outputC = []
        for feature in self.featureC:
            dataList = feature.backspaceTimeCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.backspaceTimeCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "BackspaceTime")

        outputC = []
        for feature in self.featureC:
            dataList = feature.questionmarkDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.questionmarkDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "Questionmark")

        outputC = []
        for feature in self.featureC:
            dataList = feature.suspensionpointDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.suspensionpointDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "SuspensionPoint")

        outputC = []
        for feature in self.featureC:
            dataList = feature.pointsDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.pointsDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "PointsDensity")

        outputC = []
        for feature in self.featureC:
            dataList = feature.capitalLetterDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.capitalLetterDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "CapitalLetter")

        outputC = []
        for feature in self.featureC:
            dataList = feature.nonalphabeticDensityCalc()
            mean = np.mean(dataList)
            outputC.append(mean)
        outputR = []
        for feature in self.featureR:
            dataList = feature.nonalphabeticDensityCalc()
            mean = np.mean(dataList)
            outputR.append(mean)
        self.independentTtest(outputC, outputR, "NonAlphabetic")

    def independentTtest(self, data1, data2, feature):
        """
            This method calculates the t-test for two independent samples.

            Parameters:
            data1 (string): The list of the first data.
            data2 (string): The list of the second data.
            feature (string): The name of a feature.
        """

        # calculate means
        mean1, mean2 = mean(data1), mean(data2)
        # calculate standard errors
        se1, se2 = sem(data1), sem(data2)
        # standard error on the difference between the samples
        sed = np.sqrt(se1 ** 2.0 + se2 ** 2.0)
        # calculate the t statistic
        t_stat = abs((mean1 - mean2)) / sed
        # degrees of freedom
        df = len(data1) + len(data2) - 2
        # calculate the critical value
        cv = stats.t.ppf(1.0 - self.alpha, df)
        # calculate the p-value
        p = (1.0 - stats.t.cdf(abs(t_stat), df)) * 2.0

        print("feature = ", feature)
        print('t=%.3f, df=%d, cv=%.3f, p=%.3f' % (t_stat, df, cv, p))
        # self.result += ('t=%.3f, df=%d, cv=%.3f, p=%.3f\n' % (t_stat, df, cv, p))
        self.result += 'Feature = ' + feature + '\n'
        self.result += 'The obtained Students t value is ' + str(round(t_stat, 3)) + '\n'
        self.result += 'From the t table with 95% confidence level and ' + str(df) \
                       + ' degree of freedom, the t-distribution critical value is ' + str(round(cv, 3)) + '\n'
        # interpret via p value
        '''if p > self.alpha:
            print('Accept null hypothesis that the means are equal.')
        else:
            print('Reject the null hypothesis that the means are equal.')'''

        # interpret via critical value
        if abs(t_stat) <= cv:
            print('Accept null hypothesis that the means are equal for ' + feature)
            self.result += 'Hence, accept null hypothesis that the means are equal\n'
        else:
            print('Reject the null hypothesis that the means are equal for ' + feature)
            self.result += 'Hence, reject null hypothesis that the means are equal\n'

        '''
        # compare samples using library
        stat, p = stats.ttest_ind(data1, data2)
        print('t=%.3f, p=%.3f' % (stat, p))
        self.result += ('t=%.3f, p=%.3f\n' % (stat, p))
        if p > self.alpha:
            print('Accept null hypothesis that the means are equal for ' + feature)
            self.result += 'Accept null hypothesis that the means are equal for the feature ' + feature + '\n'
        else:
            print('Reject the null hypothesis that the means are equal for ' + feature)
            self.result += 'Reject null hypothesis that the means are equal for the feature ' + feature + '\n'
        '''

        print("\n")
        self.result += '\n\n'
