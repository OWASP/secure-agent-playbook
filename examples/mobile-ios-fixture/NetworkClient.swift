import Foundation

class NetworkClient: NSObject, URLSessionDelegate {
    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        // MASVS-NETWORK-1: blindly trust any server
        if let serverTrust = challenge.protectionSpace.serverTrust {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        }
    }

    func storeKey() {
        // MASVS-STORAGE-1: secret in NSUserDefaults
        UserDefaults.standard.set("hunter2", forKey: "api_key")
    }
}
