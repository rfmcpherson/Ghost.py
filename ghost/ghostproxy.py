#
# Copyright (C) 2009, 2010 Nokia Corporation and/or its subsidiary(-ies)
# Copyright (C) 2009, 2010 Holger Hans Peter Freyther
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY APPLE COMPUTER, INC. ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE COMPUTER, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from PySide.QtNetwork import QNetworkRequest, QNetworkReply

class GhostNetworkReply(QNetworkReply):
    def __init__(self, parent, reply):
        QNetworkReply.__init__(self, parent)
        self.reply = reply # The QNetworkReply we're wrapping
        self.content = '' # All of the content
        self.data = '' # The read QIODevice data

        self.reply.metaDataChanged.connect(self.applyMetaData)
        self.reply.readyRead.connect(self.readInternal)
        self.reply.error.connect(self.errorInternal)

        self.reply.finished.connect(self.finished)
        self.reply.uploadProgress.connect(self.uploadProgress)
        self.reply.downloadProgress.connect(self.downloadProgress)

        self.setOpenMode(QNetworkReply.ReadOnly | QNetworkReply.Unbuffered)

    def abort(self):
        self.reply.abort()

    def close(self):
        return self.reply.close()

    def operation(self):
        return self.reply.operation()

    def request(self):
        return self.reply.request()
        
    def url(self):
        return self.reply.url()

    def isSequential(self):
        return self.reply.isSequential()

    def setReadBufferSize(self, size):
        super(setReadBufferSize, size)
        self.reply.setReadBufferSize(size)


    def bytesAvailable(self):
        return len(self.data) + QNetworkReply.bytesAvailable(self)

    def readData(self, size):
        size = min(size, len(self.data))
        data = self.data[:size]
        self.data = self.data[size:]
        return str(data)

    def ignoreSslErrors(self):
        self.reply.ignoreSslErrors()

    def applyMetaData(self):
        for header in self.reply.rawHeaderList():
            self.setRawHeader(header, self.reply.rawHeader(header))

        self.setHeader(
            QNetworkRequest.ContentTypeHeader, 
            self.reply.header(QNetworkRequest.ContentTypeHeader))
        self.setHeader(
            QNetworkRequest.ContentLengthHeader, 
            self.reply.header(QNetworkRequest.ContentLengthHeader))
        self.setHeader(
            QNetworkRequest.LocationHeader, 
            self.reply.header(QNetworkRequest.LocationHeader))
        self.setHeader(
            QNetworkRequest.LastModifiedHeader, 
            self.reply.header(QNetworkRequest.LastModifiedHeader))
        self.setHeader(
            QNetworkRequest.SetCookieHeader, 
            self.reply.header(QNetworkRequest.SetCookieHeader))

        self.setAttribute(
            QNetworkRequest.HttpStatusCodeAttribute, 
            self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        self.setAttribute(
            QNetworkRequest.HttpReasonPhraseAttribute, 
            self.reply.attribute(QNetworkRequest.HttpReasonPhraseAttribute))
        self.setAttribute(
            QNetworkRequest.RedirectionTargetAttribute, 
            self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute))
        self.setAttribute(
            QNetworkRequest.ConnectionEncryptedAttribute, 
            self.reply.attribute(QNetworkRequest.ConnectionEncryptedAttribute))
        self.setAttribute(
            QNetworkRequest.CacheLoadControlAttribute, 
            self.reply.attribute(QNetworkRequest.CacheLoadControlAttribute))
        self.setAttribute(
            QNetworkRequest.CacheSaveControlAttribute, 
            self.reply.attribute(QNetworkRequest.CacheSaveControlAttribute))
        self.setAttribute(
            QNetworkRequest.SourceIsFromCacheAttribute, 
            self.reply.attribute(QNetworkRequest.SourceIsFromCacheAttribute))
        self.setAttribute(
            QNetworkRequest.DoNotBufferUploadDataAttribute, 
            self.reply.attribute(QNetworkRequest.DoNotBufferUploadDataAttribute))
        self.metaDataChanged.emit()

    def errorInternal(self, err):
        self.setError(err, self.errorString())
        self.error.emit(err)

    def readInternal(self):
        buff = self.reply.readAll()
        self.content += buff
        self.data += buff
        self.readyRead.emit()

    def readAllData(self):
        return str(self.content)

