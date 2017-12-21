;;; ultan.el --- emacs interface to the ultan identifier server. -*- lexical-binding: t -*-
;;
;; Copyright (c) 2017 Austin Bingham
;;
;; Author: Austin Bingham <austin.bingham@gmail.com>
;; Version: 0.0.1
;; URL: https://github.com/abingham/emacs-ultan
;; Package-Requires: ((dash "20171028.854") (deferred "20170901.630") (request "20170131.1747") (request-deferred "20160419.1605"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;; Description:
;;
;; ultan is an identifier server for Python.
;;
;; For more details, see the project page at
;; https://github.com/abingham/ultan.
;;
;;; License:
;;
;; Permission is hereby granted, free of charge, to any person
;; obtaining a copy of this software and associated documentation
;; files (the "Software"), to deal in the Software without
;; restriction, including without limitation the rights to use, copy,
;; modify, merge, publish, distribute, sublicense, and/or sell copies
;; of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;;
;; The above copyright notice and this permission notice shall be
;; included in all copies or substantial portions of the Software.
;;
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
;; EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
;; MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
;; NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
;; BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
;; ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
;; CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
;; SOFTWARE.

;;; Code:

(require 'cl)
(require 'dash)
(require 'deferred)
(require 'json)
(require 'request)
(require 'request-deferred)

(defgroup ultan nil
  "A Python identifier server."
  :group 'tools
  :group 'programming)

(defconst ultan-host "127.0.0.1"
  "The host on which the ultan server is running.")

(defconst ultan-port "12345"
  "The port on which the ultan server is listening.")

(defun ultan-get-names (pattern)
  "Get names matching `pattern'.
  "
  (lexical-let ((data (list (cons "pattern" pattern))))
    (deferred:$
      (ultan--deferred-request
       "/get_names"
       :params data))))

;;;###autoload
(defun ultan-list-names (pattern)
  "Basic debugging tool to see what comes out of the server."
  (interactive
   (list
    (read-string "Pattern: ")))
  (deferred:$
    (ultan-get-names pattern)
    (deferred:nextc it
      (lambda (rsp)
        (let* ((response (request-response-data rsp))
               (buff (get-buffer-create "*ultan-listing*")))
          (with-current-buffer buff
            (erase-buffer)
            (-map
             (lambda (name)
               (insert name)
               (insert "\n"))
             response)))))))

(defun ultan--construct-url (location)
  "Construct a URL to a specific location on the ultan server.

  In short: http://server_host:server_port<location>
  "
  (concat "http://" ultan-host ":" ultan-port location))

(defun* ultan--deferred-request (location &key (type "GET") (data '()) (params '()))
  (let ((request-backend 'url-retrieve))
    (request-deferred
     (ultan--construct-url location)
     :type type
     :parser 'json-read
     :params params
     :headers '(("Content-Type" . "application/json"))
     :data (json-encode data))))

(provide 'ultan)

;;; ultan.el ends here
